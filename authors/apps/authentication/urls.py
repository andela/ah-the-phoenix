from django.urls import path
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    PasswordResetView, PasswordUpdateView, VerifyAPIView,
    SocialAuthenticationView, FollowUnfollowAPIView, FollowerFollowingAPIView,
    ProfileRetrieveUpdateAPIView, ProfileGetAPIView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='user_url'),
    path('users/', RegistrationAPIView.as_view(), name='user_signup'),
    path('users/login/', LoginAPIView.as_view(), name='user_login'),
    path('users/verify/<token>/',
         VerifyAPIView.as_view(), name='verify_email'),
    path('users/password_reset/',
         PasswordResetView.as_view(), name='reset_password'),
    path('users/password_update/<token>',
         PasswordUpdateView.as_view(), name='update_password'),
    path('social/login/', SocialAuthenticationView.as_view(), name='social'),
    path('profiles/<id>/follow/',
         FollowUnfollowAPIView.as_view(), name="follow"),
    path('profiles/<id>/following/',
         FollowerFollowingAPIView.as_view(), name="following"),
    path('profiles/', ProfileGetAPIView.as_view(), name='get_profiles'),
    path('profiles/<pk>/',
         ProfileRetrieveUpdateAPIView.as_view(), name='user_profile')
]
