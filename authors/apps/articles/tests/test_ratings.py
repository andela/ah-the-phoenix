from authors.apps.authentication.tests.base_test import BaseTest

from rest_framework import status


class TestArticleRatings(BaseTest):
    def rate_an_article(self, user, rating):
        token = self.authenticate_user(user).data["token"]
        article_url = self.rate_article_url()
        response = self.client.post(article_url,
                                    {"user_rating": rating},
                                    format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        return response

    def test_successful_article_rate(self):
        """users should be able to rate an article"""
        response = self.rate_an_article(self.auth_user_data, 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"],
                         "Rating submitted sucessfully")

    def test_exceed_maximum_rating(self):
        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.client.post(self.rate_article_url(),
                                    {"user_rating": 6},
                                    format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        error_message = response.data["errors"]["user_rating"][0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_message, 'The maximum allowed rating is 5')

    def test_under_minimum_rating(self):
        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.client.post(self.rate_article_url(),
                                    {"user_rating": 0},
                                    format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        error_message = response.data["errors"]["user_rating"][0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_message, "The minimum allowed rating is 1")

    def test_get_not_rated_article_ratings(self):
        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.client.get(self.rate_article_url(),
                                   HTTP_AUTHORIZATION=f'token {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["user_rating"], None)

    def test_get_rated_article(self):
        self.rate_an_article(self.auth_user_data, 2)
        token = self.authenticate_user(self.auth_user_data).data["token"]
        article_url = self.rate_article_url()
        response = self.client.get(article_url,
                                   HTTP_AUTHORIZATION=f'token {token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existant_articles_ratings(self):
        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.client.get(self.non_existant_article_url,
                                   HTTP_AUTHORIZATION=f'token {token}')
        error_message = response.data["errors"]["message"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_message, "Article not found")

    def test_get_rated_article_without_authentication(self):
        response = self.client.get(self.rate_article_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_rating"],
                         'Kindly login to rate an article')

    def test_rating_you_own_article(self):
        response = self.rate_an_article(self.auth_user2_data, 2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"],
                         "You cannot rate your own article")

    def test_rate_article_without_authentication(self):
        response = self.client.post(self.rate_article_url(),
                                    {"user_rating": 3},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"],
                         "Please login to rate an article")

    def test_rate_a_rated_article(self):
        self.rate_an_article(self.auth_user_data, 2)
        response = self.rate_an_article(self.auth_user3_data, 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"],
                         "Rating submitted sucessfully")
        self.assertDictEqual(response.data["data"], {
            "article": "rate-this",
            "user_rating": 3.0,
            "average_rating": 2.5
        })
