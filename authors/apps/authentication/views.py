import jwt
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt
import os
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from datetime import datetime, timedelta

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, PasswordResetSerializer, EmailSerializer
)
from authors.settings import SECRET_KEY
from authors import settings
from .models import User
from .mail import MailSender

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
            'exp': datetime.utcnow()
            + timedelta(minutes=60)
        }
        token = jwt.encode(payload, settings.SECRET_KEY,
                           algorithm='HS256').decode('utf-8')
        sender = os.getenv('EMAIL_HOST_USER')
        site_link = get_current_site(request)
        verification_link = 'http://' + site_link.domain + \
            f'/api/v1/users/verify/{token}'

        email_subject = "Author's Haven Email verification"
        message = render_to_string('verification_template.html', {
            'title': email_subject,
            'username': username,
            'verification_link': verification_link
        })

        send_mail(email_subject, '', sender, [email, ], html_message=message)

        serializer.save()
        message = {
            "message": "User successfully created. Check email for verification link",
            "user_info": serializer.data,
            "token": token
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
                    'message': 'Account already activated. Click on the link to continue',
                    'login link': 'http://' + site_link.domain + '/api/v1/users/login'
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            user.is_verified = True
            user.save()

            message = {
                'message': f'Welcome {username}, Your email has been successfully activated'
            }
            return Response(message, status=status.HTTP_200_OK)

        except Exception:
            message = {
                'error': 'Verification email is not valid. Try again'
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
            return Response({"message": "Email field cannot be blank"}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
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
