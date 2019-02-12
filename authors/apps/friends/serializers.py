from rest_framework import serializers

from authors.apps.authentication.models import User


class FollowerFollowingSerializer(serializers.ModelSerializer):
    """Serializer that return username"""
    class Meta:
        model = User
        fields = ('username', )


class FollowUnfollowSerializer(serializers.ModelSerializer):
    """Serializer that returns id, username, followers, following"""

    followers_total = serializers.SerializerMethodField()
    following_total = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'followers_total', 'following_total',
        )

    def get_followers_total(self, obj):
        """Returns total number of followers"""
        return obj.followers.count()

    def get_following_total(self, obj):
        """Returns number of users one is following"""
        return obj.following.count()
