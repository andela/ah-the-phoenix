from rest_framework import status
from django.urls import reverse

from authors.apps.authentication.tests.base_test import BaseTest


class CommentsTestCase(BaseTest):
    """This is the comments test case.

    It inherits the BaseTest class and contains test scenarios
    for the comment CRUD views
    """

    def create_comment(self, method, comment=None):
        """This method creates a comment and returns a Response"""
        token = self.authenticate_user(self.auth_user_data).data['token']
        response = self.client.post(self.articles_url,
                                    self.article,
                                    format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')

        comments_url = reverse('articles:comments-all', kwargs={
            'pk': response.data['slug']
        })

        if method == "POST":
            response = self.client.post(comments_url,
                                        comment,
                                        format='json',
                                        HTTP_AUTHORIZATION=f'token {token}')
        elif method == "GET":
            response = self.client.get(comments_url,
                                       format='json',
                                       HTTP_AUTHORIZATION=f'token {token}')
        elif method == "GET_404":
            response1 = self.client.post(self.articles_url,
                                         self.test_article,
                                         format='json',
                                         HTTP_AUTHORIZATION=f'token {token}')

            no_comments_url = reverse('articles:comments-all', kwargs={
                'pk': response1.data['slug']
            })
            response = self.client.get(no_comments_url,
                                       format='json',
                                       HTTP_AUTHORIZATION=f'token {token}')
        elif method == "POST_404_ARTICLE":
            unavailable_article_url = reverse('articles:comments-all', kwargs={
                'pk': 'how-are-you'
            })
            response = self.client.post(unavailable_article_url,
                                        comment,
                                        format='json',
                                        HTTP_AUTHORIZATION=f'token {token}')
        return response

    def test_can_create_comment_201(self):
        """Test whether API can create a comment successfully"""
        response = self.create_comment('POST', self.comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('body', response.data)

    def test_create_comment_with_blank_body(self):
        """Test whether API can create a comment successfully"""
        response = self.create_comment('POST', self.blank_comment)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_create_comment_to_unavailable_article(self):
        """Test whether API can create a comment successfully"""
        response = self.create_comment('POST_404_ARTICLE', self.comment)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_can_get_all_article_comments(self):
        """Test whether API can get all article comments"""
        response = self.create_comment('GET')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['Comments'], list)

    def test_can_get_all_comments_if_none(self):
        """Test whether API can get all article comments"""
        response = self.create_comment('GET_404')
        self.assertEqual(len(response.data['Comments']), 0)

    def single_comment_crud(self, method, token):
        response = self.create_comment('POST', self.comment)
        comment_url = reverse('articles:single-comment', kwargs={
            'pk': response.data['article_id'],
            'id': response.data['id']
        })
        comment_404_url = reverse('articles:single-comment', kwargs={
            'pk': response.data['article_id'],
            'id': 400
        })
        nonint_comment_url = reverse('articles:single-comment', kwargs={
            'pk': response.data['article_id'],
            'id': 'ire'
        })
        if method == "GET":
            response = self.client.get(comment_url,
                                       format='json',
                                       HTTP_AUTHORIZATION=f'token {token}')
        elif method == "PUT":
            response = self.client.put(comment_url,
                                       {
                                           "body": "This is an update"
                                       },
                                       format='json',
                                       HTTP_AUTHORIZATION=f'token {token}')
        elif method == "DELETE":
            response = self.client.delete(comment_url,
                                          format='json',
                                          HTTP_AUTHORIZATION=f'token {token}')
        elif method == "GET_404_COMMENT":
            response = self.client.get(comment_404_url,
                                       format='json',
                                       HTTP_AUTHORIZATION=f'token {token}')
        elif method == "GET_NONINT_COMMENT":
            response = self.client.get(nonint_comment_url,
                                       format='json',
                                       HTTP_AUTHORIZATION=f'token {token}')
        elif method == "PUT_404_COMMENT":
            response = self.client.put(comment_404_url,
                                       format='json',
                                       HTTP_AUTHORIZATION=f'token {token}')
        elif method == "PUT_NONINT_COMMENT":
            response = self.client.put(nonint_comment_url,
                                       format='json',
                                       HTTP_AUTHORIZATION=f'token {token}')
        elif method == "DELETE_404_COMMENT":
            response = self.client.delete(comment_404_url,
                                          format='json',
                                          HTTP_AUTHORIZATION=f'token {token}')

        elif method == "DELETE_NONINT_COMMENT":
            response = self.client.delete(nonint_comment_url,
                                          format='json',
                                          HTTP_AUTHORIZATION=f'token {token}')
        elif method == "POST":
            response = self.client.post(comment_url,
                                        {
                                            "body": "This is a reply"
                                        },
                                        format='json',
                                        HTTP_AUTHORIZATION=f'token {token}')
        elif method == "POST_400":
            res = self.client.post(comment_url,
                                   {
                                       "body": "This is a reply"
                                   },
                                   format='json',
                                   HTTP_AUTHORIZATION=f'token {token}')
            reply_comment_url = reverse('articles:single-comment', kwargs={
                'pk': response.data['article_id'],
                'id': res.data['id']
            })
            response = self.client.post(reply_comment_url,
                                        {
                                            "body": "A reply to a reply"
                                        },
                                        format='json',
                                        HTTP_AUTHORIZATION=f'token {token}')
        return response

    def test_can_get_one_comment(self):
        """Test whether API can get one comment"""
        token = self.authenticate_user(self.auth_user_data).data['token']
        response = self.single_comment_crud("GET", token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("body", response.data)

    def test_can_update_comment(self):
        """Test whether API can update a comment"""
        token = self.authenticate_user(self.auth_user_data).data['token']
        response = self.single_comment_crud("PUT", token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'],
                         'This is an update')

    def test_can_delete_comment(self):
        """Test whether API can delete a comment"""
        token = self.authenticate_user(self.auth_user_data).data['token']
        response = self.single_comment_crud("DELETE", token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'Comment deleted successfully')

    def test_cannot_update_unauthored_comment(self):
        """Token that API rejects when one attempts to update a comment
        they did not author"""
        token = self.authenticate_user(self.user_data).data['token']
        response = self.single_comment_crud("PUT", token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'],
                         'You are not the author of this comment')

    def test_cannot_delete_unauthored_comment(self):
        """Token that API rejects when one attempts to delete a comment
        they did not author"""
        token = self.authenticate_user(self.user_data).data['token']
        response = self.single_comment_crud("DELETE", token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'],
                         'You are not the author of this comment')

    def test_cannot_update_nonexistent_comment(self):
        """Token that API rejects when one attempts to update a comment
        that does not exist"""
        token = self.authenticate_user(self.user_data).data['token']
        response = self.single_comment_crud("PUT_404_COMMENT", token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'],
                         'Comment does not exist')

    def test_cannot_delete_nonexistent_comment(self):
        """Token that API rejects when one attempts to delete a comment
        that does not exist"""
        token = self.authenticate_user(self.user_data).data['token']
        response = self.single_comment_crud("DELETE_404_COMMENT", token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'],
                         'Comment does not exist')

    def test_cannot_get_nonint_commentid(self):
        """Token that API rejects when one attempts to delete provided a
        nonint comment id"""
        token = self.authenticate_user(self.user_data).data['token']
        response = self.single_comment_crud("GET_NONINT_COMMENT", token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_put_nonint_commentid(self):
        """Token that API rejects when one attempts to delete provided a
        nonint comment id"""
        token = self.authenticate_user(self.user_data).data['token']
        response = self.single_comment_crud("PUT_NONINT_COMMENT", token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete_nonint_commentid(self):
        """Token that API rejects when one attempts to delete provided a
        nonint comment id"""
        token = self.authenticate_user(self.user_data).data['token']
        response = self.single_comment_crud("DELETE_NONINT_COMMENT", token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_get_unavailable_comment(self):
        """Test whether API can get one comment"""
        token = self.authenticate_user(self.auth_user_data).data['token']
        response = self.single_comment_crud("GET_404_COMMENT", token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Comment does not exist")

    def test_can_create_child_comment(self):
        """Test that API can create comment replies"""
        token = self.authenticate_user(self.auth_user_data).data['token']
        response = self.single_comment_crud("POST", token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_reply_to_a_reply(self):
        """Test that API cannot create comment replies to replies"""
        token = self.authenticate_user(self.auth_user_data).data['token']
        response = self.single_comment_crud("POST_400", token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
