from rest_framework.views import status

from authors.apps.authentication.tests.base_test import BaseTest
from ..models import User


class TestLogin(BaseTest):

    """Test for the login functionality of the app."""

    def test_successful_user_login(self):
        """Test for a successful user login."""
        response = self.authenticate_user(self.auth_user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "pherndegz@gmail.com")
        self.assertIn("token", response.data)

    def test_wrong_email_login(self):
        """Test for a login with a wrong email."""
        self.signup_a_user(self.user_data)
        response = self.login_a_user(self.user_wrong_email_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["error"],
                         ["A user with this email and password was not found."]
                         )
        self.assertNotIn("token", response.data)

    def test_wrong_password_login(self):
        """Test for a login with a wrong password."""
        self.signup_a_user(self.user_data)
        response = self.login_a_user(self.user_wrong_password_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["error"],
                         ["A user with this email and password was not found."]
                         )
        self.assertNotIn("token", response.data)

    def test_blank_email_login(self):
        """Test for a login with a blank email."""
        self.signup_a_user(self.user_data)
        response = self.login_a_user(self.user_blank_email_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]
                         ["email"], ["This field may not be blank."])
        self.assertNotIn("token", response.data)

    def test_blank_password_login(self):
        """Test for a login with a blank password."""
        self.signup_a_user(self.user_data)
        response = self.login_a_user(self.user_blank_password_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["errors"]["password"], [
                "This field may not be blank."]
        )
        self.assertNotIn("token", response.data)

    def test_login_with_unverified_email(self):
        """Test for a login with an unverified email"""
        self.signup_a_user(self.user_data)
        user = User.objects.get(email=self.user_data['user']['email'])
        user.is_verified = False
        user.save()
        response = self.client.post(self.login_url,
                                    self.user_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["errors"]['error'], [
                "Verify email before logging in."]
        )
        self.assertNotIn("token", response.data)
