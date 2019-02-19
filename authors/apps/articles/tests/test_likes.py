from rest_framework.views import status
from authors.apps.authentication.tests.base_test import BaseTest


class TestLikeDislikeCase(BaseTest):
    def test_successfully_like_article(self):
        """Test successful liking of an article."""
        response = self.create_and_like_article()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, response.data['likes_count'])

    def test_successfully_dislike_article(self):
        """Test successful disliking of an article."""
        response = self.create_and_dislike_article()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, response.data['dislikes_count'])

    def test_like_non_existent_article(self):
        """Test liking of a non-existent article."""
        token = self.authenticate_user().data['token']
        response = self.client.patch(BaseTest.likes_article_url('james-sav'),
                                     format='json',
                                     HTTP_AUTHORIZATION=f'Token {token}'
                                     )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            "The article does not exist",
            response.data['detail'])

    def test_dislike_non_existent_article(self):
        """Test disliking of a non-existent article."""
        token = self.authenticate_user().data['token']
        response = self.client.patch(BaseTest.dislikes_article_url('jame'),
                                     format='json',
                                     HTTP_AUTHORIZATION=f'Token {token}'
                                     )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            "The article does not exist",
            response.data['detail'])

    def test_like_already_liked_article(self):
        """Test liking of an already liked article."""
        token = self.authenticate_user().data['token']
        slug = self.create_article()
        self.client.patch(BaseTest.likes_article_url(slug),
                          format='json',
                          HTTP_AUTHORIZATION=f'Token {token}'
                          )
        response = self.client.patch(BaseTest.likes_article_url(slug),
                                     format='json',
                                     HTTP_AUTHORIZATION=f'Token {token}'
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, response.data['likes_count'])

    def test_dislike_already_liked_article(self):
        """Test disliking of an already liked article."""
        token = self.authenticate_user().data['token']
        slug = self.create_article()
        self.client.patch(BaseTest.likes_article_url(slug),
                          format='json',
                          HTTP_AUTHORIZATION=f'Token {token}'
                          )
        response = self.client.patch(BaseTest.dislikes_article_url(slug),
                                     format='json',
                                     HTTP_AUTHORIZATION=f'Token {token}'
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, response.data['likes_count'])
        self.assertEqual(1, response.data['dislikes_count'])

    def test_dislike_already_disliked_article(self):
        """Test disliking of an already disliked article."""
        token = self.authenticate_user().data['token']
        slug = self.create_article()
        self.client.patch(BaseTest.dislikes_article_url(slug),
                          format='json',
                          HTTP_AUTHORIZATION=f'Token {token}'
                          )
        response = self.client.patch(BaseTest.dislikes_article_url(slug),
                                     format='json',
                                     HTTP_AUTHORIZATION=f'Token {token}'
                                     )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, response.data['dislikes_count'])
