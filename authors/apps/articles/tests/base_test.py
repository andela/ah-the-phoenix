from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.urls import reverse


class BaseTest(APITestCase):
    """Initiate data required to run the tests"""

    def setUp(self):
        """set up data for running tests"""
        self.login_url = reverse('authentication:user_login')
        self.signup_url = reverse('authentication:user_signup')
        self.articles_url = reverse('articles:articles')
        self.user = {
            "user": {
                "username": "dummy",
                "email": "dummy@gmail.com",
                "password": "Dummy@123"
            }
        }

        self.user_login = {
            "user": {
                "email": "dummy@gmail.com",
                "password": "Dummy@123"                
            }
        }

        self.article = {
                "title": "the andela way",
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
        

        self.client = APIClient()
    
    def sign_up_user(self, data):
        """register user"""
        return self.client.post(self.signup_url, data, format='json')

    def login_user(self, data):
        """login a user"""
        return self.client.post(self.login_url, data, format='json')

    def permit_user(self, user_details):
        """sign up and login user to get token"""
        self.sign_up_user(data=self.user)
        payload = self.login_user(data=user_details)
        self.client.credentials(HTTP_AUTHORIZATION='token' + payload.data['token'])
        

         

