from django.shortcuts import render

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


from authors.apps.core.permissions import IsOwnerOrReadOnly

from .models import Article
from .serializers import ArticleSerializer
from .renderers import ArticleJsonRenderer


def get_article(slug):

    try:
        article = Article.objects.get(slug=slug)

    except Exception:
        return Response(
            {"error": "Article not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    return article


class ArticleList(ListCreateAPIView):
    """Allows user to post and view a list of articles"""

    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJsonRenderer,)
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        """create an article"""
        article = request.data
        serializer = self.serializer_class(
            data=article, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetail(RetrieveUpdateDestroyAPIView):
    """Allows user to get, update and delete an article"""

    lookup_field = 'slug'
    queryset = Article.objects.all()
    renderer_classes = (ArticleJsonRenderer,)
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get(self, request, slug):
        """
        Returns article with the given slug if exists
        or returns an exception if no article with slug exists
        """
        article = get_article(slug)

        return super().get(request, slug)

    def update(self, request, slug):
        """
        Update an article
        """
        article = get_article(slug)

        article_data = request.data.get('article', {})
        serializer = self.serializer_class(
        article, data=article_data, partial=True)

        if serializer.is_valid():
            self.check_object_permissions(request, article)
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug):
        """Allows user to partially update article"""
        article = get_article(slug)

        article_data = request.data
        serializer = self.serializer_class(instance=article, data=article_data, partial=False)
        if serializer.is_valid():
            self.check_object_permissions(request, article)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, slug):
        """user can delete article"""
        if not get_article(slug):
            article_not_found()

        super().delete(self, request, slug)
        return Response({"message": "article deleted successfully"})
