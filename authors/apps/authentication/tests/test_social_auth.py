from rest_framework.views import status

from .base_test import BaseTest


class TestSocialAuthentication(BaseTest):
    def bad_400_request(self, data, error_key, message=None):
        """Tests for all 400 Bad Requests"""
        response = self.client.post(
            self.social_authentication_url, data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data[error_key])
        if message:
            self.assertIn(message.encode(), response.content)

    def ok_200_request(self, data, key):
        """Tests for all 200 OK requests"""
        response = self.client.post(
            self.social_authentication_url, data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[key])

    def test_successful_social_login(self):
        """Test for successful social oauth login"""

        self.ok_200_request(self.oauth2_data, "username")

    def test_login_empty_token(self):
        """Test for empty token"""

        self.bad_400_request(self.empty_token, "errors")

    def test_invalid_token(self):
        """Test for invalid token"""
        message = "The token provided is invalid"
        self.bad_400_request(self.invalid_token, "error", message)

    def test_wrong_provider(self):
        """Test for when provider is invalid"""
        message = "The client provider is invalid"
        self.bad_400_request(self.invalid_provider_data, "error", message)

    def test_empty_provider_data(self):
        """Test for when no provider is given"""
        message = "This field is required"
        self.bad_400_request(self.empty_provider_data, "errors", message)
