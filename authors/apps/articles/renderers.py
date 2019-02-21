import json
from rest_framework import renderers


class ArticleJsonRenderer(renderers.BaseRenderer):
    """
    Renders an article into a list or single article
    """
    media_type = 'application/json'
    format = 'json'
    charset = 'utf-8'

    def render(self, data, valid_media_type=None, renderer_context=None):
        """render a list of articles"""
        if isinstance(data, list):
            return json.dumps({'articles': data})

        else:
            """
            renders a single article or
            """
            error = data.get('detail')
            if error:
                return json.dumps({'message': data})

            return json.dumps({'article': data})


class FavoriteJsonRenderer(renderers.BaseRenderer):
    """
    Renders a list of article favorites
    """
    media_type = 'application/json'
    format = 'json'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None,
               renderer_context=None):
        """
        Render a list of article favorites
        """
        if isinstance(data, list):
            return json.dumps(
                {'favorites': data})
        if "error" in data:
            return json.dumps({'message': data})

        return json.dumps(data)
