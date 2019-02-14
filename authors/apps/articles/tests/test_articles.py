<<<<<<< HEAD
from rest_framework import status

from authors.apps.authentication.tests.base_test import BaseTest

=======
from authors.apps.authentication.tests.base_test import BaseTest

from rest_framework import status
>>>>>>> feature(authors haven): create the article rating feature

class TestArticles(BaseTest):
    def test_create_article(self):
        """users should be able to create an article"""

        token = self.authenticate_user().data["token"]
<<<<<<< HEAD
        response = self.client.post(self.articles_url,
                                    self.article,
                                    format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
=======
        response = self.client.post(self.articles_url, 
                                    self.article, 
                                    format='json', HTTP_AUTHORIZATION=f'token {token}')
>>>>>>> feature(authors haven): create the article rating feature
        new_slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_slug, "the-andela-way")

<<<<<<< HEAD
    def test_add_blank_title(self):
        """user should not be allowed to create a blank title"""

        token = self.authenticate_user().data["token"]
        response = self.client.post(self.articles_url,
                                    self.blank_title,
                                    format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = response.data["errors"]["title"][0]
        self.assertEqual(message, "This field may not be blank.")

    def test_add_blank_body(self):
        """user should not be allowed to create a blank body"""

        token = self.authenticate_user().data["token"]
        response = self.client.post(self.articles_url,
                                    self.blank_body,
                                    format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = response.data["errors"]["body"][0]
        self.assertEqual(message, "This field may not be blank.")

    def test_get_articles_logged_in(self):
        """Registered users can view articles logged in"""
        self.authenticate_user().data["token"]
        response = self.client.get(self.articles_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_articles_not_logged_in(self):
        """Unregistered users can view articles"""
        response = self.client.get(self.articles_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_article(self):
        """User can view a selected article"""
        token = self.authenticate_user().data["token"]
        response = self.client.post(self.articles_url,
                                    self.article, format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        new_slug = response.data['slug']
        response2 = self.client.get(self.articles_url + new_slug + '/',
                                    HTTP_AUTHORIZATION=f'token {token}')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_get_single_article_not_logged_in(self):
        """Unregistered user can view selected article"""
        token = self.authenticate_user().data["token"]
        response = self.client.post(self.articles_url,
                                    self.article, format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        new_slug = response.data['slug']
        self.client.credentials()
        response2 = self.client.get(self.articles_url + new_slug + '/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_create_unauthorized_article(self):
        """unregistered user cannot create articles"""

        response = self.client.post(self.articles_url,
                                    self.article,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        message = response.data["detail"]
        self.assertEqual(
            message, "Authentication credentials were not provided.")

    def test_update_article(self):
        """user is able to update theoir article"""
        token = self.authenticate_user().data["token"]
        response = self.client.post(self.articles_url,
                                    self.article, format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        new_slug = response.data['slug']
        response2 = self.client.put(self.articles_url + new_slug + '/',
                                    self.update_article, format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        new_title = response2.data["title"]
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(new_title, "Update: the andela way")

    def test_partially_update_article(self):
        """user is able to update theoir article"""
        token = self.authenticate_user().data["token"]
        response = self.client.post(self.articles_url,
                                    self.article, format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        new_slug = response.data['slug']
        response2 = self.client.patch(self.articles_url + new_slug + '/',
                                      self.update_partial_article,
                                      format='json',
                                      HTTP_AUTHORIZATION=f'token {token}')
        new_body = response2.data["body"]
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(new_body, "this is andela")

    def test_update_article_unauthorized(self):
        """user is unable update their article without authorization"""

        token = self.authenticate_user().data["token"]
        response = self.client.post(self.articles_url,
                                    self.article, format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        new_slug = response.data['slug']
        self.client.credentials()
        response2 = self.client.put(self.articles_url + new_slug + '/',
                                    self.update_article, format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        message = response2.data["detail"]
        self.assertEqual(message,
                         "Authentication credentials were not provided.")

    def test_delete_article(self):
        """User is able to delete articles"""

        token = self.authenticate_user().data["token"]
        response = self.client.post(self.articles_url,
                                    self.article, format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        new_slug = response.data['slug']
        response2 = self.client.delete(self.articles_url + new_slug + '/',
                                       HTTP_AUTHORIZATION=f'token {token}')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        message = response2.data["message"]
        self.assertEqual(message,
                         "article deleted successfully")

    def test_delete_nonexistent_article(self):
        """User is not able to delete non-existent article"""

        token = self.authenticate_user().data["token"]
        response = self.client.delete(self.articles_url +
                                      "no-article-with-slug/",
                                      format='json',
                                      HTTP_AUTHORIZATION=f'token {token}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        message = response.data["detail"]
        self.assertEqual(message,
                         "Not found.")

    def test_delete_article_unauthorized(self):
        """
        This method tests if a non owner can delete an article
        """
        token = self.authenticate_user().data["token"]
        response = self.client.post(self.articles_url,
                                    self.article, format='json',
                                    HTTP_AUTHORIZATION=f'token {token}')
        new_slug = response.data['slug']
        self.client.credentials()
        response2 = self.client.delete(self.articles_url + new_slug + '/')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        response_message = response2.data["detail"]
        self.assertEqual(response_message,
                         "Authentication credentials were not provided.")

    def test_get_article_nonexistent(self):
        """
        User cannot view an article that does not exist
        """
        self.authenticate_user().data["token"]
        response = self.client.get(self.articles_url + "no-article-with-slug/",
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        message = response.data["detail"]
        self.assertEqual(message,
                         "Not found.")
=======
    # def test_create_article_duplicate_title(self):
    #     """users should be able to create an article"""

    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     self.client.post(self.articles_url, 
    #                     self.article, 
    #                     format='json', HTTP_AUTHORIZATION=f'token {token}')
    #     response = self.client.post(self.articles_url, 
    #                                 self.article, 
    #                                 format='json', HTTP_AUTHORIZATION=f'token {token}')
    #     new_slug = response.data['slug']
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(new_slug, "the-andela-way-1")

    # def test_add_blank_title(self):
    #     """user should not be allowed to create a blank title"""

    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.post(self.articles_url, 
    #                                 self.blank_title, 
    #                                 format='json', HTTP_AUTHORIZATION=f'token {token}')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     message = response.data["errors"]["title"][0]
    #     self.assertEqual(message, "This field may not be blank.")

    # def test_add_blank_body(self):
    #     """user should not be allowed to create a blank body"""

    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.post(self.articles_url, 
    #                                 self.blank_body, 
    #                                 format='json', HTTP_AUTHORIZATION=f'token {token}')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     message = response.data["errors"]["body"][0]
    #     self.assertEqual(message, "This field may not be blank.")

    # def test_get_articles_logged_in(self):
    #     """Registered users can view articles logged in"""
    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.get(self.articles_url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_articles_not_logged_in(self):
    #     """Unregistered users can view articles"""
    #     response = self.client.get(self.articles_url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_single_article(self):
    #     """User can view a selected article"""
    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.post(self.articles_url,
    #                                 self.article, format='json',
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     new_slug = response.data['slug']
    #     response2 = self.client.get(self.articles_url + new_slug + '/',
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     self.assertEqual(response2.status_code, status.HTTP_200_OK)

    # def test_get_single_article_not_logged_in(self):
    #     """Unregistered user can view selected article"""
    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.post(self.articles_url,
    #                                 self.article, format='json',
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     new_slug = response.data['slug']
    #     self.client.credentials()
    #     response2 = self.client.get(self.articles_url + new_slug + '/')
    #     self.assertEqual(response2.status_code, status.HTTP_200_OK)




    # def test_create_unauthorized_article(self):
    #     """unregistered user cannot create articles"""

    #     response = self.client.post(self.articles_url, 
    #                                 self.article, 
    #                                 format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     message = response.data["detail"]
    #     self.assertEqual(message, "Authentication credentials were not provided.")

    # def test_update_article(self):
    #     """user is able to update theoir article"""
    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.post(self.articles_url,
    #                                 self.article, format='json', 
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     new_slug = response.data['slug']
    #     response2 = self.client.put(self.articles_url + new_slug + '/',
    #                                 self.update_article, format='json',
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     new_title = response2.data["title"]
    #     self.assertEqual(response2.status_code, status.HTTP_200_OK)
    #     self.assertEqual(new_title, "Update: the andela way")

    # def test_partially_update_article(self):
    #     """user is able to update theoir article"""
    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.post(self.articles_url,
    #                                 self.article, format='json', 
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     new_slug = response.data['slug']
    #     response2 = self.client.patch(self.articles_url + new_slug + '/',
    #                                 self.update_partial_article, format='json',
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     new_body = response2.data["body"]
    #     self.assertEqual(response2.status_code, status.HTTP_200_OK)
    #     self.assertEqual(new_body, "this is andela")

    # def test_update_article_unauthorized(self):
    #     """user is unable update their article without authorization"""

    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.post(self.articles_url,
    #                                 self.article, format='json', 
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     new_slug = response.data['slug']
    #     self.client.credentials()
    #     response2 = self.client.put(self.articles_url + new_slug + '/',
    #                                 self.update_article, format='json')
    #     self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
    #     message = response2.data["detail"]
    #     self.assertEqual(message,
    #                      "Authentication credentials were not provided.")


    # def test_delete_article(self):
    #     """User is able to delete articles"""

    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.post(self.articles_url,
    #                                 self.article, format='json',
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     new_slug = response.data['slug']
    #     response2 = self.client.delete(self.articles_url + new_slug + '/',
    #                                     HTTP_AUTHORIZATION=f'token {token}')
    #     self.assertEqual(response2.status_code, status.HTTP_200_OK)
    #     message = response2.data["message"]
    #     self.assertEqual(message,
    #                     "article deleted successfully")
    
    # def test_delete_nonexistent_article(self):
    #     """User is not able to delete non-existent article"""

    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.delete(self.articles_url + "no-article-with-slug/",
    #                                 format='json',
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     message = response.data["detail"]
    #     self.assertEqual(message,
    #                      "Not found.")


        

    # def test_delete_article_unauthorized(self):
    #     """
    #     This method tests if a non owner can delete an article
    #     """
    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.post(self.articles_url,
    #                                 self.article, format='json',
    #                                 HTTP_AUTHORIZATION=f'token {token}')
    #     new_slug = response.data['slug']
    #     self.client.credentials()
    #     response2 = self.client.delete(self.articles_url + new_slug + '/')
    #     self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
    #     response_message = response2.data["detail"]
    #     self.assertEqual(response_message,
    #                     "Authentication credentials were not provided.")

    # def test_get_article_nonexistent(self):
    #     """
    #     User cannot view an article that does not exist
    #     """
    #     self.sign_up_user(self.user)
    #     user = self.login_user(self.user_login)
    #     token = user.data["token"]
    #     response = self.client.get(self.articles_url + "no-article-with-slug/",
    #                                format='json')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     message = response.data["detail"]
    #     self.assertEqual(message,
    #                      "Not found.")    
>>>>>>> feature(authors haven): create the article rating feature
