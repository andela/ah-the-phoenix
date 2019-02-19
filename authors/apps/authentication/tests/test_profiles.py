from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.views import status
from django.urls import reverse

from ..models import User
from .base_test import BaseTest


class ProfilesTestCase(BaseTest):

    """Test all the user profile functionalities"""

    def test_view_a_user_profile(self):
        """Test creation and getting of a user profile"""
        url = self.get_single_profile_url()
        response = self.verify_user(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_non_existent_profile(self):
        """Test getting of a user profile that doesnt exist"""
        url = self.profile_url + str(2555) + "/"
        response = self.verify_user(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_all_users_profiles(self):
        """Test viewing of all the users"""
        url = self.profile_url
        response = self.verify_user(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_a_user_can_edit_their_profile(self):
        """Test whether a user can successfully edit their profile"""
        self.signup_a_user(self.user_data)
        user = self.login_a_user(self.user_login_data)
        token = user.data["token"]
        url = self.get_single_profile_url()
        response = self.client.patch(url,
                                     HTTP_AUTHORIZATION=f'token {token}',
                                     data=self.new_profile,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_a_user_cannot_edit_others_profiles(self):
        """
        Test whether a user cannot successfully edit
        another user's profile
        """
        self.signup_a_user(self.user_data)
        user = self.login_a_user(self.user_login_data)
        token = user.data["token"]
        url = self.profile_url + str(3) + "/"
        response = self.client.patch(url,
                                     HTTP_AUTHORIZATION=f'token {token}',
                                     data=self.new_profile,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_makes_notification_subscription_when_subscribed(self):
        """Test for when a user makes a notification subscription when already
            subscribed"""

        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.client.put(self.subscribe_url,
                                   format='json',
                                   HTTP_AUTHORIZATION=f'token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_makes_notification_subscription(self):
        """Test for when a user makes a notification subscription"""

        token = self.authenticate_user(self.auth_user_data).data["token"]
        user = User.objects.get(email=self.auth_user_data['user']['email'])
        user.get_notifications = False
        user.save()
        response = self.client.put(self.subscribe_url,
                                   format='json',
                                   HTTP_AUTHORIZATION=f'token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_makes_notification_unsubscription(self):
        """Test for when a user makes a notification unsubscription"""

        token = self.authenticate_user(self.auth_user_data).data["token"]
        user = User.objects.get(email=self.auth_user_data['user']['email'])
        uuid = urlsafe_base64_encode(force_bytes(user)
                                     ).decode("utf-8")

        unsubscribe_url = reverse('authentication:unsubscribe', kwargs={
            "uuid": uuid
        })
        response = self.client.put(unsubscribe_url,
                                   format='json',
                                   HTTP_AUTHORIZATION=f'token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_makes_notification_unsubscription_when_unsubscribed(self):
        """Test for when a user makes a notification unsubscription when
            already unsubscribed
            """

        token = self.authenticate_user(self.auth_user_data).data["token"]
        user = User.objects.get(email=self.auth_user_data['user']['email'])
        uuid = urlsafe_base64_encode(force_bytes(user)
                                     ).decode("utf-8")

        unsubscribe_url = reverse('authentication:unsubscribe', kwargs={
            "uuid": uuid
        })
        self.client.put(unsubscribe_url,
                        format='json',
                        HTTP_AUTHORIZATION=f'token {token}')
        response = self.client.put(unsubscribe_url,
                                   format='json',
                                   HTTP_AUTHORIZATION=f'token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
