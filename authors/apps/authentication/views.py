from __future__ import unicode_literals
from rest_framework.generics import (
    RetrieveUpdateAPIView, CreateAPIView,
    UpdateAPIView, ListAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from rest_framework import generics, status
from rest_framework.exceptions import NotFound

from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import MissingBackend
from social_django.utils import load_backend, load_strategy

from .renderers import UserJSONRenderer
from authors.settings import SECRET_KEY     # noqa F401
from authors import settings            # noqa F401
from .models import User
from .mail import MailSender
from .serializers import (EmailSerializer, LoginSerializer,
                          PasswordResetSerializer, RegistrationSerializer,
                          SocialAuthenticationSerializer, UserSerializer,
                          ProfilesSerializer,
                          FollowerFollowingSerializer,
                          FollowUnfollowSerializer,
                          SubscriptionSerializer)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email', None)
        username = serializer.validated_data.get('username')

        payload = {
            'email': email,
            'username': username,
            'exp': datetime.utcnow() + timedelta(minutes=60)
        }
        token = jwt.encode(payload, settings.SECRET_KEY,
                           algorithm='HS256').decode('utf-8')
        sender = os.getenv('EMAIL_HOST_USER')
        link = "https://the-phoenix-frontend-staging.herokuapp.com/" + \
            f"verify/{token}"

        email_subject = "Author's Haven Email verification"
        message = render_to_string('verification_template.html', {
            'title': email_subject,
            'username': username,
            'verification_link': link
        })

        send_mail(email_subject, '', sender, [email, ], html_message=message)

        serializer.save()
        message = {
            "message": "User successfully created. Check email for "
            "verification link",
            "user_id": serializer.data['id']
        }

        return Response(message, status=status.HTTP_201_CREATED)


class VerifyAPIView(APIView):

    serializer_class = UserSerializer
    def get(self, request, token):

        try:
            email = jwt.decode(token, settings.SECRET_KEY)['email']
            user = User.objects.get(email=email)
            username = jwt.decode(token, settings.SECRET_KEY)['username']

            if user.is_verified:
                site_link = get_current_site(request)
                message = {
                    'message': 'Account already activated. '
                               'Click on the link to continue',
                    'login link': 'http://' + site_link.domain +
                                  '/api/v1/users/login'
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            user.is_verified = True
            user.save()

            message = {
                'message': f'Welcome {username}, '
                           'Your email has been successfully activated'
            }
            return Response(message, status=status.HTTP_200_OK)

        except Exception:
            message = {
                'error': 'Verification token is not valid. Try again'
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = EmailSerializer

    def post(self, request):
        recipient = request.data.get('email', {})
        if not recipient:
            return Response({"message": "Email field cannot be blank"},
                            status=status.HTTP_400_BAD_REQUEST)

        token = jwt.encode({"email": recipient},
                           settings.SECRET_KEY, algorithm='HS256')

        is_user_exising = User.objects.filter(email=recipient).exists()
        if is_user_exising:
            result = MailSender.send_email_message(recipient, token, request)
            return Response(result, status=status.HTTP_200_OK)

        else:
            result = {
                'message': 'A user with the given email was not found'
            }
            return Response(result, status=status.HTTP_404_NOT_FOUND)


class PasswordUpdateView(UpdateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def update(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:
            return Response({"message": "Passwords do not match"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data={
            "password": password
        })
        serializer.is_valid(raise_exception=True)

        try:
            decode_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=decode_token['email'])
            user.set_password(password)
            user.save()
            result = {'message': 'Your password has successfully been reset'}
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)


class SocialAuthenticationView(CreateAPIView):
    """Authenticates a user using social media sites"""
    permission_classes = (AllowAny,)
    serializer_class = SocialAuthenticationSerializer
    renderer_classes = (UserJSONRenderer,)

    def create(self, request):
        """Receives a provider and access token for authentication"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_provider = serializer.data.get("client_provider", None)
        strategy = load_strategy(request)

        if request.user.is_anonymous:
            user = None
        else:
            user = request.user

        # Load data from backend with associated provider
        try:
            backend = load_backend(strategy=strategy, name=client_provider,
                                   redirect_uri=None)
            if isinstance(backend, BaseOAuth1):
                if "access_token_secret" in request.data:
                    access_token = {
                        'oauth_token': request.data['access_token'],
                        'oauth_token_secret':
                        request.data['access_token_secret']
                    }
                else:
                    return Response(
                        {"error": "You require an access token secret"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            elif isinstance(backend, BaseOAuth2):
                access_token = request.data["access_token"]

        except MissingBackend:
            return Response({"error": "The client provider is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Use pipeline to create the user if details don't exist
        try:

            authenticated_user = backend.do_auth(access_token, user=user)

        except BaseException as e:
            return Response({"error": "The token provided is invalid",
                             "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
            email = authenticated_user.email
            username = authenticated_user.username
            token = authenticated_user.token
            user_data = {
                "user_id": authenticated_user.id,
                "username": username,
                "email": email,
                "token": token
            }
            return Response(user_data, status=status.HTTP_200_OK)


class FollowUnfollowAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    APIView for following a user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, id, format=None):
        """
        This method create a user relationship btween the user
        with the username passed in and the user sending the
        request
        """
        try:
            to_be_followed = User.objects.get(pk=id)
        except Exception:
            return Response({
                'error': "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if not to_be_followed.is_verified:
            return Response({
                'error': "User not verified"
            }, status=status.HTTP_404_NOT_FOUND)

        if request.user == to_be_followed:
            message = {
                "error": "You cannot follow yourself"
            }
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            already_followed = request.user.following.filter(pk=id).exists()
            if already_followed:
                return Response({
                    'error': 'You already follow this user'
                },
                    status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({
                'error': 'Error when following',
                'message': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request.user.following.add(to_be_followed)
        request.user.save()

        serializer = FollowUnfollowSerializer(request.user)
        message = {
            "message": "Profile successfully followed",
            "user": serializer.data
        }
        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        """
        Deletes a follow relationship between the user sending the
        request and the user with the username passed
        """
        try:
            User.objects.get(pk=id)
        except Exception:
            return Response({
                'error': "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        follower = User.objects.get(pk=request.user.id)

        relationship = follower.following.filter(pk=id).exists()
        if not relationship:
            return Response(
                {
                    'error': 'You do not follow this user'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        follower.following.remove(id)
        serializer = FollowUnfollowSerializer(follower)
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
        user = get_object_or_404(User, id=self.kwargs['id'])

        followed_friends = user.following.all()
        following_friends = user.followers.all()

        return {
            "followed": followed_friends,
            "followers": following_friends
        }

    def get(self, request, id, format=None):
        """Returns the user's followed user"""

        if self.get_queryset() is not None:

            following_dict = self.get_queryset()

            follower_serializer = FollowerFollowingSerializer(
                following_dict['followed'], many=True)
            following_serializer = FollowerFollowingSerializer(
                following_dict['followers'], many=True)

            message = {
                "Followers": follower_serializer.data,
                "Following": following_serializer.data
            }
            return Response(message, status=status.HTTP_200_OK)


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ProfilesSerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            profile = User.objects.get(
                pk=pk
            )
        except Exception:
            raise NotFound("The requested profile was not found")

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        if str(request.user.id) != pk:
            response = {
                "message": "You don't have permission to edit this profile"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = self.serializer_class(instance=request.user,
                                           data=data, partial=True)
        if serializer.is_valid():
            self.check_object_permissions(request, data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileGetAPIView(ListAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = ProfilesSerializer
    queryset = User.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = ProfilesSerializer(queryset, many=True)
        return Response({"Profiles": serializer.data})


class SubscribeAPIView(APIView):
    """Allows user to subscribe or unsubscribe from notifications"""

    permission_classes = (AllowAny,)
    serializer_class = SubscriptionSerializer

    def put(self, request):
        user = User.objects.get(email=request.user.email)
        if not user.get_notifications:
            user.get_notifications = True
            user.save()
            return Response({
                "message": "You have successfully subscribed"
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                "Message": "You are already subscribed"
            }, status=status.HTTP_400_BAD_REQUEST)


class UnsubscribeAPIView(APIView):
    "Allows user to unsubscribe to notifications"

    permission_classes = (AllowAny,)

    serializer_class = SubscriptionSerializer

    def put(self, request, uuid):
        username = force_text(urlsafe_base64_decode(uuid))
        user = User.objects.get(username=username)
        if user.get_notifications:
            user.get_notifications = False
            user.save()
            return Response({
                "message": "You have successfully unsubscribed"
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                "Message": "You are not subscribed"
            }, status=status.HTTP_400_BAD_REQUEST)
