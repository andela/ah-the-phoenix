from rest_framework.views import status

from authors.apps.authentication.tests.base_test import BaseTest


class TestLogin(BaseTest):

    """Test for the login functionality of the app."""

    def test_successful_user_login(self):
        """Test for a successful user login."""
        self.signup_a_user(self.user_data)
        response = self.login_a_user(self.user_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "jam@gmail.com")

    def test_wrong_email_login(self):
        """Test for a login with a wrong email."""
        self.signup_a_user(self.user_data)
        response = self.login_a_user(self.user_wrong_email_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["error"],
                         ["A user with this email and password was not found."]
                         )

    def test_wrong_password_login(self):
        """Test for a login with a wrong password."""
        self.signup_a_user(self.user_data)
        response = self.login_a_user(self.user_wrong_password_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["error"],
                         ["A user with this email and password was not found."]
                         )

    def test_blank_email_login(self):
        """Test for a login with a blank email."""
        self.signup_a_user(self.user_data)
        response = self.login_a_user(self.user_blank_email_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]
                         ["email"], ["This field may not be blank."])

    def test_blank_password_login(self):
        """Test for a login with a blank password."""
        self.signup_a_user(self.user_data)
        response = self.login_a_user(self.user_blank_password_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["errors"]["password"], [
                "This field may not be blank."]
        )
