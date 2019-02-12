from rest_framework import status

from authors.apps.friends.tests.basetest import BaseTest


class FollowUnfollowTestCase(BaseTest):
    """
    This class creates a testcase for follow and unfollow functionality
    """

    def test_successful_follow(self):
        """Test whether API user can follow another successfully"""
        token = self.signup_user()
        self.create_test_user()
        response = self.follow_user('kim', token)
        self.assertEqual(response.data['message'],
                         "Profile successfully followed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_unavailable_user(self):
        """Test whether API user can follow an unavailable user"""
        token = self.signup_user()
        response = self.follow_user('Tom', token)
        self.assertEqual(response.data['error'],
                         "User not found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_yourself(self):
        """Test whether API user can follow oneself"""
        token = self.signup_user()
        response = self.follow_user('Sam', token)
        self.assertEqual(response.data['error'],
                         "You cannot follow yourself")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_follow_user_already_folowed(self):
        """Test whether API user can follow a user they already follow"""
        token = self.signup_user()
        self.create_test_user()
        self.follow_user('kim', token)
        response = self.follow_user('kim', token)
        self.assertEqual(response.data['error'],
                         "You already follow this user")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_successful_unfollow(self):
        """Test whether API user can unfollow a follower successfully"""
        token = self.signup_user()
        self.create_test_user()
        self.follow_user('kim', token)
        response = self.unfollow_user('kim', token)
        self.assertEqual(response.data['message'],
                         "Profile successfully unfollowed")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_unavailable_user(self):
        """Test whether API user can unfollow a follower successfully"""
        token = self.signup_user()
        response = self.unfollow_user('kim', token)
        self.assertEqual(response.data['error'],
                         "User not found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unfollow_nonfollower(self):
        """Test whether API user can unfollow a user they don't follow"""
        token = self.signup_user()
        self.create_test_user()
        response = self.unfollow_user('kim', token)
        self.assertEqual(response.data['error'],
                         "You do not follow this user")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_following(self):
        """Test whether API user can follow another successfully"""
        token = self.signup_user()
        self.create_test_user()
        self.follow_user('kim', token)
        response = self.get_following('Sam', token)
        self.assertIsInstance(response.data['Followers'], list)
        self.assertIsInstance(response.data['Following'], list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
