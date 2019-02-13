import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """Token authentication using JWT."""

    authentication_header_prefix = 'token'

    def authenticate(self, request):
        """Checks authorization on every request."""

        request.user = None
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            message = "Invalid token header. No credentials provided."
            raise exceptions.AuthenticationFailed(message)
        if len(auth_header) > 2:
            message = "Invalid token header. "
            "Token should not contain whitespaces."
            raise exceptions.AuthenticationFailed(message)

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != self.authentication_header_prefix:
            message = "Invalid token header. Token header should"
            " include the word `token` followed by a whitespace"
            raise exceptions.AuthenticationFailed(message)

        return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        """Authenticate the provided credentials."""

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except User.DoesNotExist:
            message = "Could not decode token"
            raise exceptions.AuthenticationFailed(message)

        try:
            user = User.objects.get(username=payload['username'])
        except exceptions.AuthenticationFailed:
            message = "No user matching this token was found"
            raise exceptions.AuthenticationFailed(message)

        return (user, token)
