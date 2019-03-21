from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .serializers import NotificationSerializer
# from .signal import *
from .renderers import NotificationJSONRenderer


class NotificationViewList(APIView):
    '''
    get all notifications where the receiver was the current user
    '''
    permission_classes = (IsAuthenticated,)
    renderer_classes = (NotificationJSONRenderer,)
    serializer_class = NotificationSerializer

    def get(self, request):
        queryset = self.request.user.notifications.all().order_by('-timestamp')

        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}
        )
        serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleNotification(APIView):
    "get single notification"
    permission_classes = (IsAuthenticated,)
    renderer_classes = (NotificationJSONRenderer,)
    serializer_class = NotificationSerializer

    def get(self, request, id):
        try:
            notification = self.request.user.notifications.all().filter(
                id=id).first()
        except Exception:
            raise Http404('Error when retrieving notification')

        if not notification:
            return Response({'error': 'Notification not found'},
                            status.HTTP_404_NOT_FOUND)
        else:
            if notification.unread:
                notification.mark_as_read()

        serializer = self.serializer_class(
            notification,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
