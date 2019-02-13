from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import serializers, status
from django.db.models import Avg
from .serializers import RatingSerializer
from .models import Article, Rating

class RatingAPIView(GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_class = (IsAuthenticatedOrReadOnly,)

    def get_article(self, slug):
        """Returns an article based on slug."""
        article = Article.objects.all().filter(slug=slug).first()
        return article

    def get_rating(self, user, article):
        """Returns an articles's rating."""
        try:
            return Rating.objects.get(user=user, article=article)
        except Rating.DoesNotExist:
            raise NotFound(
                detail={"rating": "You have not yet rated this article"}
            )

    def post(self, request, slug):
        """POST request to rate an article."""
        rating = request.data
        article = self.get_article(slug)

        if not article:
            raise ValidationError(
                detail={'message': 'Article not found'}
            )

        if request.user.id == article.author.id:
            return Response({
                "message": "You cannot rate your own article"
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            current_rating = Rating.objects.get(
                user = request.user.id,
                article = article.id
            )
            serializer = self.serializer_class(
            current_rating, data = rating)
        except Rating.DoesNotExist:
            serializer = self.serializer_class(data = rating)

        serializer.is_valid(raise_exception = True)
        serializer.save(user = request.user, article = article)

        return Response({
            'message': 'Rating submitted sucessfully',
            'data': serializer.data
        }, status = status.HTTP_201_CREATED)

    def get(self, request, slug):
        """Get request for an article ratings."""
        article = self.get_article(slug)
        rating = None

        if not article:
            raise ValidationError(
                detail={'message': 'Article not found'}
            )

        if request.user.is_authenticated:
            rating = Rating.objects.get(user=request.user, article=article)

        if rating is None:
            average = Rating.objects.filter(
                article=article).aggregate(Avg('user_rating')
                )
            average_rating = average['user_rating__avg']