from authors.apps.authentication.tests.base_test import BaseTest

from rest_framework import status


class TestFavoriteArticle(BaseTest):
    """Tests for favoriting articles."""
    def favorite_article(self, user):
        """Favorites an existing article."""
        token = self.authenticate_user(user).data["token"]
        response = self.client.put(
            self.favorite_article_url(), HTTP_AUTHORIZATION=f'token {token}'
        )
        return response

    def test_favorite_article_successfully(self):
        """A user should be able to favorite an article."""
        response = self.favorite_article(self.auth_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {"message": "article added to favorites"})

    def test_favorite_article_twice(self):
        """A user cannot favorite an article twice"""
        self.favorite_article(self.auth_user_data)
        response = self.favorite_article(self.auth_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {"error": "you have already favorited this article"})

    def test_unsuccessful_unfavorite(self):
        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.client.delete(
            self.favorite_article_url(), HTTP_AUTHORIZATION=f'token {token}'
        )
        self.assertEqual(
            response.data, {"message": "article not in favorites"})

    def test_successful_unfavorite(self):
        self.favorite_article(self.auth_user_data)
        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.client.delete(
            self.favorite_article_url(), HTTP_AUTHORIZATION=f'token {token}'
        )
        self.assertEqual(
            response.data, {"message": "article removed from favorites"})

    def test_get_zero_favorited_articles(self):
        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.client.get(
            self.favorites_url, HTTP_AUTHORIZATION=f'token {token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_get_favorited_articles(self):
        self.favorite_article(self.auth_user_data)
        token = self.authenticate_user(self.auth_user_data).data["token"]
        response = self.client.get(
           self.favorites_url, HTTP_AUTHORIZATION=f'token {token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{
            'article_slug': 'rate-this',
            'title': 'rate this',
            'description': 'to be used in rating tests',
            'body': 'whose afraid of the big bad wolf?'
            }])
