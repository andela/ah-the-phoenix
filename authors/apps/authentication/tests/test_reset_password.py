from rest_framework.views import status
from django.urls import reverse

from .base_test import BaseTest


class TestEmailPasswordReset(BaseTest):

    """Tests for all password reset and updating functionality."""

    def test_successful_email_sending(self):
        """Test for successful mail sending."""
        self.signup_a_user(self.user_data)
        response = self.send_reset_password_email(self.email_forgot_password)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            b'A password reset link has been sent to your email', response.content)

    def test_if_user_email_exists(self):
        """Test if the email given is for an existent user."""
        response = self.send_reset_password_email(self.email_forgot_password)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(b"A user with the given email was not found", response.content)


class TestEmailPasswordUpdate(BaseTest):
    def password_url_call(self):
        """Helper function to ensure code reuse for other tests."""
        return self.client.put(BaseTest.create_url(),
                                   data=self.passwords,
                                   format='json')
    def base_password_update(self, message, password, confirm_password):
        """Run the test functionality for other tests."""
        TestEmailPasswordReset.test_successful_email_sending(self)
        self.passwords['password'] = password
        self.passwords['confirm_password'] = confirm_password
        response = self.password_url_call()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(message.encode(), response.content)

    def test_password_reset_valid_password(self):
        """Test that a user with valid credentials can reset password."""
        TestEmailPasswordReset.test_successful_email_sending(self)
        response = self.password_url_call()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'Your password has successfully been reset', response.content)

    def test_passwords_differing(self):
        """Test if the passwords given are different."""
        message = "Passwords do not match"
        self.base_password_update(message, 'jamessavalij', 'jamessavali')

