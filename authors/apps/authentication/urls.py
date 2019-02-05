from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='get_users'),
    path('users/', RegistrationAPIView.as_view(), name='user_signup'),
    path('users/login/', LoginAPIView.as_view(), name='user_login'),
]
