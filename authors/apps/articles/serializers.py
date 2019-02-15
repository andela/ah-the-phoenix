from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from .models import Article, Rating


class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    title = serializers.CharField(
        required=True,
        max_length=500,
        error_messages={
            'required': 'title cannot be empty',
            'max_length': 'title cannot exceed 500 characters'
        })

    description = serializers.CharField(
        required=False,
        max_length=1000,
        error_messages={
            'max_length': 'description cannot exceed 1000 characters'
        })

    body = serializers.CharField(
        required=True,
        error_messages={
            'required': 'the body cannot be empty'
        }
    )

    def retrieve_author(self, obj):
        """retrieve the author profile"""
        pass

    class Meta:
        model = Article
        fields = ('slug', 'title', 'description',
                  'body', 'image', 'created_at', 'updated_at')


class RatingSerializer(serializers.ModelSerializer):
    """Serializers for the rating model"""
    max_rating = 5
    min_rating = 1
    user_rating = serializers.FloatField(
        required=True,
        validators=[
            MinValueValidator(
                min_rating, message="The minimum allowed rating is 1"),
            MaxValueValidator(
                max_rating, message="The maximum allowed rating is 5")
        ],
        error_messages={
            "required": "Please provide a rating between 1 and 5"
        }
    )
    article = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        """Returns the average rating for an article"""
        average_rating = Rating.objects.filter(
            article=obj.article).aggregate(Avg('user_rating'))
        return average_rating["user_rating__avg"]

    def get_article(self, obj):
        """Returns an article that matches the slug"""
        return obj.article.slug

    class Meta:
        model = Rating
        fields = ("article", "user_rating", "average_rating")
