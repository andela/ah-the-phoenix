from django.urls import path

from .views import NotificationViewList, SingleNotification

urlpatterns = [
    path('notifications/', NotificationViewList.as_view(),
         name='notifications'),
    path('notifications/<id>/', SingleNotification.as_view(),
         name='single-notification')

]
