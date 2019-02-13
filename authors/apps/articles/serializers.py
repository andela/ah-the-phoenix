from rest_framework import serializers

from .models import Article

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

        



