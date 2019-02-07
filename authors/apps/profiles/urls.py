from django.urls import path

from .views import ProfileUpdateAPIView, ProfileGetAPIView

app_name = 'profiles'

urlpatterns = [
    path('profiles/', ProfileGetAPIView.as_view(), name='get_profiles'),
    path('profiles/<str:username>/', ProfileUpdateAPIView.as_view(), name='user_profile')
]