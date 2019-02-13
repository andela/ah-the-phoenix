from rest_framework import status

from authors.apps.authentication.tests.base_test import BaseTest


class TestGetUser(BaseTest):

    """Test for the login functionality of the app."""

    def test_get_users(self):
        token = self.authenticate_user().data["token"]
        response = self.client.get(self.user_url,
                                   HTTP_AUTHORIZATION=f'token {token}'
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "pherndegz@gmail.com")

    def test_wrong_token_header(self):
        token = self.authenticate_user().data["token"]
        response = self.client.get(self.user_url,
                                   HTTP_AUTHORIZATION=f'token{token}'
                                   )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_too_many_arguments_in_header(self):
        token = self.authenticate_user().data["token"]
        response = self.client.get(self.user_url,
                                   HTTP_AUTHORIZATION=f'token dd {token}'
                                   )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_token(self):

        response = self.client.get(self.user_url,
                                   HTTP_AUTHORIZATION=f'token hjdgjfg ddd'
                                   )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
