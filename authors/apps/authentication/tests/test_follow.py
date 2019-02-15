from rest_framework import status

from authors.apps.authentication.tests.base_test import BaseTest
from ..models import User


class FollowUnfollowTestCase(BaseTest):
    """
    This class creates a testcase for follow and unfollow functionality
    """

    def test_successful_follow(self):
        """Test whether API user can follow another successfully"""
        token = self.authenticate_user(self.auth_user_data).data["token"]
        test_id = self.create_test_user()
        response = self.follow_user(test_id, token)
        self.assertEqual(response.data['message'],
                         "Profile successfully followed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_unavailable_user(self):
        """Test whether API user can follow an unavailable user"""
        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.follow_user(377, token)
        self.assertEqual(response.data['error'],
                         "User not found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_yourself(self):
        """Test whether API user can follow oneself"""
        token = self.authenticate_user(self.auth_user_data).data["token"]
        user = User.objects.get(email=self.authenticate_user(
            self.auth_user_data).data["email"])
        response = self.follow_user(user.id, token)
        self.assertEqual(response.data['error'],
                         "You cannot follow yourself")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_follow_user_already_folowed(self):
        """Test whether API user can follow a user they already follow"""
        token = self.authenticate_user(self.auth_user_data).data["token"]
        test_id = self.create_test_user()
        self.follow_user(test_id, token)
        response = self.follow_user(test_id, token)
        self.assertEqual(response.data['error'],
                         "You already follow this user")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_successful_unfollow(self):
        """Test whether API user can unfollow a follower successfully"""
        token = self.authenticate_user(self.auth_user_data).data["token"]
        test_id = self.create_test_user()
        self.follow_user(test_id, token)
        response = self.unfollow_user(test_id, token)
        self.assertEqual(response.data['message'],
                         "Profile successfully unfollowed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_unavailable_user(self):
        """Test whether API user can unfollow a follower successfully"""
        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.unfollow_user(363, token)
        self.assertEqual(response.data['error'],
                         "User not found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unfollow_nonfollower(self):
        """Test whether API user can unfollow a user they don't follow"""
        token = self.authenticate_user(self.auth_user_data).data["token"]
        test_id = self.create_test_user()
        response = self.unfollow_user(test_id, token)
        self.assertEqual(response.data['error'],
                         "You do not follow this user")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_following(self):
        """Test whether API user can view follow list successfully"""
        token = self.authenticate_user(self.auth_user_data).data["token"]
        test_id = self.create_test_user()
        self.follow_user(test_id, token)
        response = self.get_following(test_id, token)
        self.assertIsInstance(response.data['Followers'], list)
        self.assertIsInstance(response.data['Following'], list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
