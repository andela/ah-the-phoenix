from django.urls import path

from authors.apps.articles import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ArticleList.as_view(), name='articles'),
    path('articles/<slug>/', views.ArticleDetail.as_view(),
         name='article-details'),
]