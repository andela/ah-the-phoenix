from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from django.db.models import Avg

from .serializers import ArticleSerializer, RatingSerializer
from .renderers import ArticleJsonRenderer
from .models import Article, Rating


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


class LikeViewSet(viewsets.ViewSet):
    serializer_class = ArticleSerializer
    permissions = (IsAuthenticatedOrReadOnly,)

    def partial_update(self, request, pk=None):
        """Update likes field."""
        try:
            article = Article.objects.get(pk=pk)
        except Exception:
            raise NotFound("The article does not exist")
        if article in Article.objects.filter(
                disliked_by=request.user):
            article.disliked_by.remove(request.user)
        if article in Article.objects.filter(
                liked_by=request.user):
            article.liked_by.remove(request.user)
        else:
            article.liked_by.add(request.user)

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
        try:
            article = Article.objects.get(pk=pk)
        except Exception:
            raise NotFound("The article does not exist")
        if article in Article.objects.filter(
                liked_by=request.user):
            article.liked_by.remove(request.user)
        if article in Article.objects.filter(
                disliked_by=request.user):
            article.disliked_by.remove(request.user)
        else:
            article.disliked_by.add(request.user)

        serializer = self.serializer_class(article,
                                           context={
                                               'request': request},
                                           partial=True)
        return Response(serializer.data, status.HTTP_200_OK)
