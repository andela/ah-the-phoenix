from django.test import TestCase

from authors.apps.authentication.models import User


class TestForUserModel(TestCase):

    """Ascertain whether the user model really works."""

    def test_create_user(self):
        """Test whether the model can successfully create a user."""
        response = User.objects.create_user(username="jey",
                                            password="password",
                                            email="jey@gmail.com")
        self.assertIsInstance(response,
                              User,)

    def test_create_user_invalid_username(self):
        """
        Test whether the model can raise errors if given invalid
        username.
        """
        with self.assertRaisesMessage(TypeError,
                                      "Users must have a username."):
            User.objects.create_user(username=None,
                                     password="password",
                                     email="jey@gmail.com")

    def test_create_user_invalid_email(self):
        """
        Test whether the model can raise errors if given invalid
        email.
        """
        with self.assertRaisesMessage(TypeError,
                                      "Users must have an email address."):
            User.objects.create_user(username="jey",
                                     password="jeymosas",
                                     email=None)
