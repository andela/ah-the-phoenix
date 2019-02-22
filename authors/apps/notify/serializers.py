from rest_framework import serializers

from authors.apps.authentication.models import User
from notifications.models import Notification
from authors.apps.authentication.serializers import UserSerializer
from authors.apps.articles.serializers import ArticleSerializer


class NotificationSerializer(serializers.ModelSerializer):
    '''
    notification serializer
    '''
    actor = UserSerializer('actor_object_id')
    action_object = ArticleSerializer('action_object_object_id')
    recipient = UserSerializer(User, read_only=True)

    class Meta:
        '''
        Notification fields to be returned to users
        '''
        model = Notification
        fields = ('id', 'actor', 'unread', 'verb', 'recipient',
                  'action_object', 'timesince')
