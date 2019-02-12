from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from authors.apps.authentication.models import User
from authors.apps.friends.models import Friend
from authors.apps.friends.serializers import (
    FollowerFollowingSerializer, FollowUnfollowSerializer
)
from authors.apps.friends.utils import Utils


class FollowUnfollowAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    APIView for following a user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, username, format=None):
        """
        This method create a user relationship btween the user
        with the username passed in and the user sending the
        request
        """
        try:
            to_be_followed = User.objects.get(username=username)
        except Exception:
            return Response({
                'error': "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        follower = User.objects.get(pk=request.user.id)

        if follower == to_be_followed:
            message = {
                "error": "You cannot follow yourself"
            }
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)

        user_followed, created_now = Friend.objects.get_or_create(
            follower=follower, followed=to_be_followed
        )
        if created_now is False:
            return Response({'error': 'You already follow this user'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = FollowUnfollowSerializer(to_be_followed)
        message = {
            "message": "Profile successfully followed",
            "user": serializer.data
        }
        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, username, format=None):
        """
        Deletes a follow relationship between the user sending the
        request and the user with the username passed
        """
        try:
            to_be_unfollowed = User.objects.get(username=username)
        except Exception:
            return Response({
                'error': "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        follower = User.objects.get(pk=request.user.id)

        relationship = Friend.objects.filter(
            follower=follower,
            followed=to_be_unfollowed
        )
        if not relationship:
            return Response(
                {
                    'error': 'You do not follow this user'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        relationship.delete()
        serializer = FollowUnfollowSerializer(to_be_unfollowed)
        message = {
            "message": "Profile successfully unfollowed",
            "user": serializer.data
        }
        return Response(message, status=status.HTTP_200_OK)


class FollowerFollowingAPIView(generics.ListAPIView):
    """
    This API returns a list of user followers and following
    """

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])

        followed_friends = Friend.objects.select_related(
            'followed',).filter(follower=user.id).all()
        following_friends = Friend.objects.select_related(
            'follower',).filter(followed=user.id).all()
        return {
            "followed": followed_friends,
            "followers": following_friends
        }

    def get(self, request, username, format=None):
        """Returns the user's followed user"""

        if self.get_queryset() is not None:

            followed_friend_objects = self.get_queryset()["followed"]
            following_friend_objects = self.get_queryset()["followers"]

            users_followed = [u.followed for u in followed_friend_objects]
            users_following = [u.follower for u in following_friend_objects]

            follower_serializer = FollowerFollowingSerializer(
                users_following, many=True)
            following_serializer = FollowerFollowingSerializer(
                users_followed, many=True)

            followers = Utils().create_following_list(follower_serializer.data)
            following = Utils().create_following_list(
                following_serializer.data)
            message = {
                "Followers": followers,
                "Following": following
            }
            return Response(message, status=status.HTTP_200_OK)
