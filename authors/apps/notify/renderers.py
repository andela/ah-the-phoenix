from rest_framework.renderers import JSONRenderer
import json


class NotificationJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render the articles in a structured manner for the end user.
        """
        if data is not None:
            if len(data) <= 1:
                return json.dumps({
                    'notification': data
                })
            return json.dumps({
                'notifications': data
            })
        return json.dumps({
            'notifications': 'No article found.'
        })
