from rest_framework.views import status
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
        url = self.profile_url + f"ja0mes" + "/"
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
        response = self.client.put(url,
                                   HTTP_AUTHORIZATION=f'token {token}',
                                   data=self.new_profile,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
