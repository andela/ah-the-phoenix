from django.urls import path
from .views import FollowUnfollowAPIView, FollowerFollowingAPIView

urlpatterns = [
    path('profiles/<username>/follow/',
         FollowUnfollowAPIView.as_view(), name="follow"),
    path('profiles/<username>/following/',
         FollowerFollowingAPIView.as_view(), name="following"),
]
