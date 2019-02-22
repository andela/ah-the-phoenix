from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from .models import Article, Rating, Comment, Favorite


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
    liked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    disliked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('slug', 'title', 'description',
                  'body', 'image',
                  'liked_by', 'disliked_by', 'likes_count', 'dislikes_count',
                  'created_at', 'updated_at')

    def get_likes_count(self, obj):
        return obj.liked_by.count()

    def get_dislikes_count(self, obj):
        return obj.disliked_by.count()


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
    article_slug = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_article_slug(self, obj):
        """Returns the article's slug"""
        return obj.article.slug

    def get_average_rating(self, obj):
        """Returns the average rating for an article"""
        average_rating = Rating.objects.filter(
            article=obj.article).aggregate(Avg('user_rating'))
        return average_rating["user_rating__avg"]

    class Meta:
        model = Rating
        fields = ("article_slug", "user_rating", "average_rating")


class CommentSerializer(serializers.ModelSerializer):
    """This is the serializer class for comments

    body is a required input
    """
    author_id = serializers.SerializerMethodField()
    article_id = serializers.SerializerMethodField()
    body = serializers.CharField(
        required=True,
        max_length=250,
        error_messages={
            'required': 'The comment body cannot be empty',
        }
    )

    def format_date(self, date):
        return date.strftime('%d %b %Y %H:%M:%S')

    def create_children(self, instance):
        children = [
            {
                'id': thread.id,
                'body': thread.body,
                'author': thread.author.username,
                'created_at': self.format_date(thread.created_at),
                'updated_at': self.format_date(thread.updated_at)
            } for thread in instance.children.all()
        ]
        return children

    def to_representation(self, instance):
        """For custom output"""

        children = self.create_children(instance)

        representation = super(CommentSerializer,
                               self).to_representation(instance)
        representation['created_at'] = self.format_date(instance.created_at)
        representation['updated_at'] = self.format_date(instance.updated_at)
        representation['author'] = instance.author.username
        representation['article'] = instance.article.title
        representation['reply_count'] = instance.children.count()
        representation['children'] = children

        return representation

    class Meta:
        model = Comment
        fields = (
            'id', 'article_id', 'body', 'author_id', 'created_at',
            'updated_at', 'children'
        )
        read_only_fields = (
            'id', 'created_at', 'updated_at', 'article_id',
            'author_id', 'parent', 'children'
        )

    def get_author_id(self, obj):
        """Return author username"""
        return obj.author.id

    def get_article_id(self, obj):
        """Return article """
        return obj.article.slug

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class FavoriteInputSerializer(serializers.ModelSerializer):
    """Input serializer for favoriting an article."""

    class Meta:
        model = Favorite
        fields = ('article', 'user')


class FavoriteInfoSerializer(serializers.BaseSerializer):
    """Serializer for the data to be rendered."""

    def to_representation(self, obj):
        return {
            'article_slug': obj.article.slug,
            'title': obj.article.title,
            'description': obj.article.description,
            'body': obj.article.body,
        }
