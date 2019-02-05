from rest_framework import status

from authors.apps.authentication.tests.base_test import BaseTest
from authors.apps.authentication.models import User


class TestRegistration(BaseTest):

    """Test for user registration/signup functionality."""

    def test_register_user(self):
        """Test for successful user registration."""
        response = self.signup_a_user(self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "jam@gmail.com")

    def test_registeration_no_username(self):
        """Test for user registration if the username field is left blank."""
        response = self.signup_a_user(self.user_lacks_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["username"],
                         ["This field may not be blank."]
                         )

    def test_registeration_no_email(self):
        """Test for user registration if the email field is left blank."""
        response = self.signup_a_user(self.user_lacks_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["email"],
                         ["This field may not be blank."]
                         )

    def test_registeration_no_password(self):
        """Test for user registration if the password field is left blank."""
        response = self.signup_a_user(self.user_lacks_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["password"],
                         ["This field may not be blank."]
                         )

    def test_registeration_invalid_email(self):
        """
        Test for user registration if the username
        given email is invalid.
        """
        response = self.signup_a_user(self.user_invalid_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["email"],
                         ["Enter a valid email address."]
                         )

    def test_registeration_short_password(self):
        """Test for user registration if a short password is given."""
        response = self.signup_a_user(self.user_short_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["errors"]["password"],
                         ["Ensure this field has at least 8 characters."]
                         )

    def test_registeration_duplicate_user_email(self):
        """Test for user registration if the email entered already exists."""
        self.signup_a_user(self.user_data)
        response_duplicate = self.signup_a_user(self.user_data_duplicate_email)
        self.assertEqual(response_duplicate.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_duplicate.data["errors"]["email"],
                         ["user with this email already exists."])

    def test_registeration_duplicate_username(self):
        """
        Test for user registration if the username
        entered already exists.
        """
        self.signup_a_user(self.user_data)
        response_duplicate = self.signup_a_user(
            self.user_data_duplicate_username)
        self.assertEqual(response_duplicate.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_duplicate.data["errors"]["username"],
                         ["user with this username already exists."])

    def test_registeration_for_a_super_user(self):
        """Test if a superuser can be successfully created."""
        admin_user = User.objects.create_superuser(
            'jey',
            'jey@gmail.com',
            'jemo'
        )
        self.assertEqual(admin_user.is_active, True)
        self.assertEqual(admin_user.is_staff, True)
        self.assertEqual(admin_user.is_superuser, True)
