from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Article, Comment, Rating, Favorite
from .renderers import ArticleJsonRenderer, FavoriteJsonRenderer
from .serializers import (
    ArticleSerializer, CommentSerializer, RatingSerializer,
    FavoriteInfoSerializer, FavoriteInputSerializer)


def get_article(slug):

    try:
        article = Article.objects.get(slug=slug)
        return article
    except Article.DoesNotExist:
        raise NotFound(
            {"error": "Article not found"}
        )


class ArticleViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJsonRenderer,)

    def list(self, request):
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, many=True)
        return Response({"Articles": serializer.data})

    def create(self, request):
        """create an article"""
        article = request.data
        serializer = self.serializer_class(
            data=article, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Returns article with the given slug if exists
        or returns an exception if no article with slug exists
        """
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update an article
        """
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        article_data = request.data.get('article', {})
        serializer = self.serializer_class(
            data=article_data, partial=False)

        if serializer.is_valid():
            self.check_object_permissions(request, article)
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        article_data = request.data
        serializer = self.serializer_class(
            instance=article, data=article_data, partial=True)
        if serializer.is_valid():
            self.check_object_permissions(request, article)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        article.delete()
        return Response({"message": "article deleted successfully"},
                        status=status.HTTP_200_OK)


class RatingAPIView(GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, slug):
        """POST request to rate an article."""
        rating = request.data
        article = get_article(slug)

        if request.user.id == article.author.id:
            return Response({
                "message": "You cannot rate your own article"
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            current_rating = Rating.objects.get(
                user=request.user.id,
                article=article
            )
            serializer = self.serializer_class(
                current_rating, data=rating)
        except Rating.DoesNotExist:
            serializer = self.serializer_class(data=rating)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, article=article)

        return Response({
            'message': 'Rating submitted sucessfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, slug):
        """Get request for an article ratings."""
        rating = None
        article = get_article(slug)

        try:
            rating = Rating.objects.get(user=request.user, article=article)
        except Exception:
            rating = None

        if rating is None:
            avg = Rating.objects.filter(
                article=article).aggregate(Avg('user_rating'))
            average_rating = avg['user_rating__avg']
            if avg["user_rating__avg"] is None:
                average_rating = 0

            if request.user.is_authenticated is False:
                return Response({
                    'article_slug': article.slug,
                    'average_rating': average_rating,
                    'user_rating': 'login to rate the article'
                }, status=status.HTTP_200_OK)

            return Response({
                'message': 'article rating',
                'data': {
                    "article_slug": article.slug,
                    'average_rating': average_rating,
                    'user_rating': 'you have not rated this article'
                }
            }, status=status.HTTP_200_OK)

        serialized_data = self.serializer_class(rating)
        return Response({
            'message': 'article rating',
            'data': serialized_data.data
        }, status=status.HTTP_200_OK)


def check_if_article_exists(request, pk, action):
    article = get_article(pk)
    if request.user in article.liked_by.all():
        request.user.likes.remove(article)
    else:
        if action == 'like':
            request.user.likes.add(article)
    if request.user in article.disliked_by.all():
        request.user.dislikes.remove(article)
    else:
        if action == 'dislike':
            request.user.dislikes.add(article)
    return article


class LikeViewSet(viewsets.ViewSet):
    serializer_class = ArticleSerializer
    permissions = (IsAuthenticatedOrReadOnly,)

    def partial_update(self, request, pk=None):
        """Update likes field."""
        article = check_if_article_exists(request, pk, 'like')
        serializer = self.serializer_class(article,
                                           context={
                                               'request': request},
                                           partial=True)
        return Response(serializer.data, status.HTTP_200_OK)


class DisLikeViewSet(viewsets.ViewSet):
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def partial_update(self, request, pk=None):
        """Update dislikes field."""
        article = check_if_article_exists(request, pk, 'dislike')

        serializer = self.serializer_class(article,
                                           context={
                                               'request': request},
                                           partial=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet):
    """Class to handle comments route'

    One can post a comment, retrieve all, retrieve one, update,
    delete comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJsonRenderer,)

    def get_specific_comment(self, article_id, comment_id, request):
        """This methos a single comment related to a specific article"""
        get_article(article_id)
        try:
            comment = Comment.objects.filter(pk=comment_id,
                                             article_id=article_id).first()
        except Exception:
            raise NotFound("Error when retrieving comment")

        if not comment:
            return Response({"error": "Comment does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        return comment

    def list(self, request, **kwargs):
        """This is the endpoint to view all article comments"""
        article_id = self.kwargs['pk']
        get_article(article_id)

        try:
            comments = Comment.objects.filter(article_id=article_id).order_by(
                '-created_at')
        except Exception:
            return Response({"error": "No comments found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(comments, many=True)
        return Response(
            {
                'Comments': serializer.data
            }
        )

    def create(self, request, **kwargs):
        """This is the view for creating a new comment"""
        article_id = self.kwargs['pk']
        article = get_article(article_id)

        comment = request.data
        serializer = self.serializer_class(
            data=comment, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, id, **kwargs):
        """This is the view for updating a comment"""
        article_id = self.kwargs['pk']
        comment = self.get_specific_comment(
            article_id, id, request
        )
        if isinstance(comment, Response):
            return comment
        serializer = self.serializer_class(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, id, **kwargs):
        """This is the view for updating a comment"""
        article_id = self.kwargs['pk']
        comment = self.get_specific_comment(
            article_id, id, request
        )
        if isinstance(comment, Response):
            return comment
        if comment.author.id != request.user.id:
            return Response({
                "error": "You are not the author of this comment"
            },
                status=status.HTTP_401_UNAUTHORIZED)
        comment_data = request.data
        serializer = self.serializer_class(
            instance=comment, data=comment_data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, id, **kwargs):
        """This is the view for deleting a comment"""
        article_id = self.kwargs['pk']
        comment = self.get_specific_comment(
            article_id, id, request
        )
        if isinstance(comment, Response):
            return comment
        if comment.author.id != request.user.id:
            return Response({
                "error": "You are not the author of this comment"
            },
                status=status.HTTP_401_UNAUTHORIZED)
        comment.delete()
        return Response({
            "message": "Comment deleted successfully"
        },
            status=status.HTTP_200_OK)

    def create_reply(self, request, id, **kwargs):
        """This is the view that handles creation of child comments"""
        article_id = self.kwargs['pk']
        comment = self.get_specific_comment(
            article_id, id, request
        )
        if isinstance(comment, Response):
            return comment
        comment_data = request.data
        article = Article.objects.get(pk=article_id)
        serializer = self.serializer_class(
            data=comment_data, context={'request': request}
        )
        if comment.parent:
            return Response({
                "error": "You cannot reply to this comment"
            },
                status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, author=request.user, parent=comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FavoriteViewSet(viewsets.ViewSet):
    """Allows addition and removal of articles from favorites"""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteInfoSerializer
    renderer_classes = (FavoriteJsonRenderer,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, slug):
        article_exists = Article.objects.filter(slug=slug).exists()
        if not article_exists:
            return({"error": "Article not found"}, status.HTTP_404_NOT_FOUND)
        article = Article.objects.get(slug=slug)
        favorite_existence = Favorite.objects.filter(
            article=article.pk, user=request.user.id).exists()
        if favorite_existence:
            return Response(
                {'error': 'you have already favorited this article'},
                status.HTTP_400_BAD_REQUEST)
        data = {"article": article.pk, "user": self.request.user.id}
        serializer = FavoriteInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'article added to favorites'},
                        status.HTTP_201_CREATED)

    def destroy(self, request, slug):
        article = get_article(slug)
        instance = Favorite.objects.filter(
            article=article.pk, user=request.user)
        if instance.exists():
            instance.delete()
            return Response({'message': 'article removed from favorites'},
                            status.HTTP_200_OK)
        return Response({'message': 'article not in favorites'},
                        status.HTTP_404_NOT_FOUND)

    def list(self, request):
        queryset = Favorite.objects.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
