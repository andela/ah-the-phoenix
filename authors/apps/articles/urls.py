from django.urls import path

from authors.apps.articles import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ArticleViewSet.as_view(
        {'get': 'list', "post": "create"}), name='articles-all'),
    path('articles/<pk>/', views.ArticleViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update",
         "delete": "destroy"}), name='single-article')
]
