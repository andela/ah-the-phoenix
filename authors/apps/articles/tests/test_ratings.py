from authors.apps.authentication.tests.base_test import BaseTest

from rest_framework import status


class TestArticleRatings(BaseTest):
    def test_successful_article_rate(self):
        """users should be able to rate an article"""

        token = self.authenticate_user(self.auth_user_data).data["token"]

