from rest_framework import status
from django.urls import reverse

from authors.apps.authentication.tests.base_test import BaseTest
from authors.apps.authentication.models import User


class TestRegistration(BaseTest):

    """Test for user registration/signup functionality."""

    def test_register_user(self):
        """Test for successful user registration."""
        response = self.signup_a_user(self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_info']["email"], "jam@gmail.com")

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

    def test_successful_email_verification(self):
        """Test if user email can be successfull verified"""

        token = self.signup_a_user(self.user_data).data['token']
        verification_url = reverse(
            'authentication:verify_email', kwargs={'token': token})

        response = self.client.get(
            verification_url,
            HTTP_AUTHORIZATION=f'token {token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_already_validated_email(self):
        """Test if user email can be successfull verified"""
        token = self.signup_a_user(self.user_data).data['token']
        verification_url = reverse(
            'authentication:verify_email', kwargs={'token': token})

        self.client.get(
            verification_url,
            HTTP_AUTHORIZATION=f'token {token}'
        )
        response_two = self.client.get(
            verification_url,
            HTTP_AUTHORIZATION=f'token {token}'
        )
        self.assertEqual(response_two.status_code, status.HTTP_403_FORBIDDEN)

    def test_verification_with_invalid_token(self):
        """Test if user email can be successfull verified"""
        token = self.signup_a_user(self.user_data).data['token']
        verification_url = reverse('authentication:verify_email', kwargs={
                                   'token': 'weucnuwencusn'})

        response = self.client.get(
            verification_url,
            HTTP_AUTHORIZATION=f'token {token}'
        )
        
    def test_registeration_for_a_super_user_no_password(self):
        """Test if superuser lacks password during registration"""
        with self.assertRaisesMessage(TypeError,
                                      'Superusers must have a password.'):
            User.objects.create_superuser(
            'jey',
            'jey@gmail.com',
            None
            )
    
    def test_invalid_password(self):
        """test if a password is valid"""
        response = self.signup_a_user(self.password_lacks_specialchar)
        self.assertEqual(response.data['errors']['password'],
                         ["please consider a password that has a number, an uppercase letter, lowercase letter and a special character"]
                         )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_nodigits(self):
        """test if username is all digits"""
        response = self.signup_a_user(self.username_nodigits)
        self.assertEqual(response.data['errors']['username'],
                         ["username is invalid"]
                         )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_username(self):
        '''test if username is too short'''
        response = self.signup_a_user(self.short_username)
        self.assertEqual(response.data['errors']['username'],
                         ["username cannot be less than 2 characters"]
                         )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
