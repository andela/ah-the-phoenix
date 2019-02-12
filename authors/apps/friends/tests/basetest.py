from rest_framework.test import APITestCase
from django.urls import reverse


class BaseTest(APITestCase):
    """
    This class defines all methods and atributes to be
    inherited by all follow-unfollow test cases
    """

    def setUp(self):
        """"
        Defines all the variables to be used in all test casses
        """
        self.signup_url = reverse("authentication:user_signup")
        self.login_url = reverse("authentication:user_login")
        self.signup_data = {
            "user": {
                "email": "sam@gmail.com",
                "username": "Sam",
                "password": "Sam123@#"
            }
        }
        self.test_user = {
            "user": {
                "email": "kimm@gmail.com",
                "username": "kim",
                "password": "Kim123@#"
            }
        }

    def signup_user(self):
        """This method registers new user and returns a token"""
        response = self.client.post(
            self.signup_url,
            self.signup_data,
            format="json"
        )
        token = response.data["user_info"]["token"]
        return token

    def create_test_user(self):
        """This method registers a test user for testcases"""
        self.client.post(
            self.signup_url,
            self.test_user,
            format="json"
        )

    def follow_user(self, username, token):
        """This method sends a follow request to a user"""
        follow_url = reverse("following:follow", kwargs={'username': username})
        response = self.client.post(
            follow_url,
            HTTP_AUTHORIZATION=f'token {token}'
        )
        return response

    def unfollow_user(self, username, token):
        """This method sends a follow request to a user"""
        follow_url = reverse("following:follow", kwargs={'username': username})
        response = self.client.delete(
            follow_url,
            HTTP_AUTHORIZATION=f'token {token}'
        )
        return response

    def get_following(self, username, token):
        """This method sends a follow request to a user"""
        following_url = reverse("following:following",
                                kwargs={'username': username})
        response = self.client.get(
            following_url,
            HTTP_AUTHORIZATION=f'token {token}'
        )
        return response
