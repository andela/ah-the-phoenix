import os
from datetime import datetime, timedelta
import jwt
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase
from ..models import User


class BaseTest(APITestCase):

    """Initiate all the data required in running other tests."""

    def setUp(self):
        """Define all variables required by other test cases."""
        self.user_url = reverse('authentication:user_url')
        self.signup_url = reverse('authentication:user_signup')
        self.login_url = reverse('authentication:user_login')
        self.password_reset_url = reverse('authentication:reset_password')
        self.articles_url = reverse('articles:articles-all')
        self.profile_url = reverse('authentication:get_profiles')
        self.favorites_url = reverse('articles:favorites')
        self.auth_user_data = {
            "user": {
                "email": "pherndegz@gmail.com",
                "password": "Jsn23$$nd",
                "username": "PaulGichuki"
            }
        }
        self.auth_user2_data = {
            "user": {
                "email": "einstein@gmail.com",
                "password": "WE12**msdd",
                "username": "madgenius"
            }
        }
        self.auth_user3_data = {
            "user": {
                "email": "neil@gmail.com",
                "password": "WE12**msdd",
                "username": "famescience"
            }
        }
        self.user_data = {
            "user": {
                "username": "James",
                "email": "wearethephoenix34@gmail.com",
                "password": "jamesSavali1"
            }
        }
        self.user2_data = {
            "user": {
                "username": "constantine",
                "email": "emporer@gmail.com",
                "password": "aC34##myndd"
            }
        }

        self.user_data_duplicate_username = {
            "user": {
                "username": "James",
                "email": "jame@gmail.com",
                "password": "jamesSavali1"
            }
        }

        self.user_data_duplicate_email = {
            "user": {
                "username": "James2",
                "email": "wearethephoenix34@gmail.com",
                "password": "jamesSavali1"
            }
        }

        self.user_lacks_username = {
            "user": {
                "username": "",
                "email": "wearethephoenix34@gmail.com",
                "password": "jamesSavali1"
            }
        }

        self.user_lacks_email = {
            "user": {
                "username": "jamesS",
                "email": "",
                "password": "jamesSavali1"
            }
        }

        self.user_lacks_password = {
            "user": {
                "username": "james2",
                "email": "wearethephoenix34@gmail.com",
                "password": ""
            }
        }

        self.user_invalid_email = {
            "user": {
                "username": "james2",
                "email": "jamgmail.com",
                "password": "kenyanchiyetu"
            }
        }

        self.user_short_password = {
            "user": {
                "username": "james2",
                "email": "wearethephoenix34@gmail.com",
                "password": "kenya"
            }
        }

        self.user_wrong_password = {
            "user": {
                "username": "james2",
                "email": "wearethephoenix34@gmail.com",
                "password": "111"
            }
        }

        self.user_login_data = {
            "user": {
                "email": "wearethephoenix34@gmail.com",
                "password": "jamesSavali1"
            }
        }

        self.user_wrong_email_login = {
            "user": {
                "email": "jamaa@gmail.com",
                "password": "jamesSavali1"
            }
        }

        self.user_wrong_password_login = {
            "user": {
                "email": "wearethephoenix34@gmail.com",
                "password": "jamesSavali2"
            }
        }

        self.user_blank_email_login = {
            "user": {
                "email": "",
                "password": "jamesSavali1"
            }
        }

        self.user_blank_password_login = {
            "user": {
                "email": "wearethephoenix34@gmail.com",
                "password": ""
            }
        }

        self.username_nodigits = {
            "user": {
                "username": "23798731",
                "email": "james@gmail.com",
                "password": "jamesSavali1#"

            }
        }

        self.short_username = {
            "user": {
                "username": "k",
                "email": "james@gmail.com",
                "password": "jamesSavali1#"

            }
        }

        self.password_lacks_specialchar = {
            "user": {
                "username": "kevinkibet",
                "email": "kevin@andela.com",
                "password": "kevinrules"
            }
        }

        self.non_superuser = {
            "user": {
                "username": "winston",
                "email": "winston@andela.com",
                "password": "Winston#67"
            }
        }
        self.article = {
            "title": "the andela way",
            "description": "andela is awesome",
            "body": "lets be epic"
        }
        self.rating_article = {
            "title": "rate this",
            "description": "to be used in rating tests",
            "body": "whose afraid of the big bad wolf?"
        }
        self.test_article = {
            "title": "this is andela",
            "description": "andela is awesome",
            "body": "lets be epic"
        }

        self.blank_title = {
            "title": "",
            "description": "andela is awesome",
            "body": "lets be epic"
        }

        self.blank_body = {
            "title": "the andela way",
            "description": "andela is awesome",
            "body": ""
        }

        self.update_article = {
            "article": {
                "title": "Update: the andela way",
                "description": "andela is awesome and EPIC",
                "body": "this is andela"
            }
        }

        self.update_partial_article = {
            "title": "Update: the andela way",
            "description": "andela is awesome and EPIC",
            "body": "this is andela"
        }

        self.social_authentication_url = reverse('authentication:social')

        self.invalid_token = 'invalidtokendonotallowdbkjs'

        self.oauth2_token = os.getenv("OAUTH2_ACCESS_TOKEN")

        self.invalid_provider_data = {
            "client_provider": "notprovider",
            "access_token": self.oauth2_token
        }

        self.invalid_token = {
            "client_provider": "facebook",
            "access_token": self.invalid_token
        }

        self.oauth2_data = {
            "client_provider": "facebook",
            "access_token": self.oauth2_token
        }

        self.empty_token = {
            "client_provider": "facebook"
        }

        self.empty_provider_data = {
            "access_token": self.oauth2_token
        }

        self.email_forgot_password = {
            "email": "wearethephoenix34@gmail.com"
        }

        self.empty_email_field = {
            "email": ""
        }

        self.passwords = {
            "password": "jamesSavali8@",
            "confirm_password": "jamesSavali8@"
        }

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

        self.email_forgot_password = {
            "email": "wearethephoenix34@gmail.com"
        }

        self.empty_email_field = {
            "email": ""
        }

        self.passwords = {
            "password": "jamesSavali8@",
            "confirm_password": "jamesSavali8@"
        }

        self.profile = {
            'profile': {
                "bio": "i am an introvert",
                "image": "https://workhound.com/05/placeholder-profile-pic.png"
            }
        }

        self.new_profile = {
            'profile': {
                "bio": "i am an extrovert",
                "image": "https://workhound.com"
            }
        }

        self.non_existant_article_url = reverse(
            "articles:rating", args=["not-existing-article"])
        # comments variables
        self.comment = {
            "body": "I am a comment"
        }
        self.blank_comment = {
            "body": ""
        }

    def rate_article_url(self):
        token = self.authenticate_user(self.auth_user2_data).data["token"]
        self.client.post(self.articles_url,
                         self.rating_article,
                         format='json',
                         HTTP_AUTHORIZATION=f'token {token}')
        rate_article_url = reverse("articles:rating", args=["rate-this"])
        return rate_article_url

    def favorite_article_url(self):
        token = self.authenticate_user(self.auth_user2_data).data["token"]
        self.client.post(self.articles_url,
                         self.rating_article,
                         format='json',
                         HTTP_AUTHORIZATION=f'token {token}')
        rate_article_url = reverse(
            "articles:favorite_article", args=["rate-this"])
        return rate_article_url

    def signup_a_user(self, user_details):
        """Invoke the server by sending a post request to the signup url."""
        return self.client.post(self.signup_url,
                                user_details,
                                format='json')

    def login_a_user(self, user_details):
        """Invoke the server by sending a post request to the login url."""
        user = User.objects.get(email=self.user_data['user']['email'])
        user.is_verified = True
        user.save()
        return self.client.post(self.login_url,
                                user_details,
                                format='json')

    def authenticate_user(self, data):
        """Invoke the server by sending a post request to the signup url."""

        self.client.post(self.signup_url,
                         data,
                         format='json')
        user = User.objects.get(email=data['user']['email'])
        user.is_verified = True
        user.save()
        response = self.client.post(self.login_url,
                                    data,
                                    format='json')
        return response

    def send_reset_password_email(self, user_details):
        """Invoke the server by sending a post request to the password reset
         url."""
        return self.client.post(self.password_reset_url,
                                user_details,
                                format='json')

    @staticmethod
    def create_url():
        """Create a url with the token, to redirect the user
         to password update."""
        token = jwt.encode({"email": "wearethephoenix34@gmail.com",
                            "iat": datetime.now(),
                            "exp": datetime.utcnow() + timedelta(minutes=5)},
                           settings.SECRET_KEY,
                           algorithm='HS256').decode()
        reset_url = reverse("authentication:update_password",
                            kwargs={"token": token})
        return reset_url

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
        res = self.client.post(
            self.signup_url,
            self.test_user,
            format="json"
        )
        user = User.objects.get(email=self.test_user['user']['email'])
        user.is_verified = True
        user.save()
        return res.data['user_id']

    def follow_user(self, id, token):
        """This method sends a follow request to a user"""
        follow_url = reverse("authentication:follow", kwargs={'id': id})
        response = self.client.post(
            follow_url,
            HTTP_AUTHORIZATION=f'token {token}'
        )
        return response

    def unfollow_user(self, id, token):
        """This method sends a follow request to a user"""
        follow_url = reverse("authentication:follow", kwargs={'id': id})
        response = self.client.delete(
            follow_url,
            HTTP_AUTHORIZATION=f'token {token}'
        )
        return response

    def get_following(self, id, token):
        """This method sends a follow request to a user"""
        following_url = reverse("authentication:following",
                                kwargs={'id': id})
        response = self.client.get(
            following_url,
            HTTP_AUTHORIZATION=f'token {token}'
        )
        return response

    def get_single_profile_url(self):
        """Return a user's profile url"""
        self.signup_a_user(self.user_data)
        email = self.user_data['user']['email']
        user_object = User.objects.get(email=email)
        user_id = str(user_object.id)
        url = self.profile_url + user_id + "/"
        return url

    def verify_user(self, uri):
        """Signup, login and get a user's profile"""
        self.signup_a_user(self.user_data)
        user = self.login_a_user(self.user_login_data)
        token = user.data["token"]
        return self.client.get(uri,
                               HTTP_AUTHORIZATION=f'token {token}')

    @staticmethod
    def likes_article_url(pk):
        """Return liking url."""
        url = reverse('articles:like_article', args=[pk])
        return url

    @staticmethod
    def dislikes_article_url(pk):
        """Return disliking url."""
        url = reverse('articles:dislike_article', args=[pk])
        return url

    def create_article(self):
        """Create an article."""
        token = self.authenticate_user(self.auth_user_data).data['token']
        article = self.client.post(self.articles_url,
                                   self.article,
                                   format='json',
                                   HTTP_AUTHORIZATION=f'Token {token}')
        slug = article.data['slug']
        return slug

    def create_and_like_article(self):
        """Create and like an article."""
        token = self.authenticate_user(self.auth_user_data).data['token']
        article = self.client.post(self.articles_url,
                                   self.article,
                                   format='json',
                                   HTTP_AUTHORIZATION=f'Token {token}')
        slug = article.data['slug']
        return self.client.patch(BaseTest.likes_article_url(slug),
                                 format='json',
                                 HTTP_AUTHORIZATION=f'Token {token}'
                                 )

    def create_and_dislike_article(self):
        """Create and dislike an article."""
        token = self.authenticate_user(self.auth_user_data).data['token']
        article = self.client.post(self.articles_url,
                                   self.article,
                                   format='json',
                                   HTTP_AUTHORIZATION=f'Token {token}')
        slug = article.data['slug']
        return self.client.patch(BaseTest.dislikes_article_url(slug),
                                 format='json',
                                 HTTP_AUTHORIZATION=f'Token {token}'
                                 )
