from django.urls import path

from authors.apps.articles import views

app_name = "articles"

urlpatterns = [
    path('articles/', views.ArticleViewSet.as_view(
        {'get': 'list', "post": "create"}), name='articles-all'),
    path('articles/<pk>/', views.ArticleViewSet.as_view(
        {"get": "retrieve", "put": "update", "patch": "partial_update",
         "delete": "destroy"}), name='single-article'),
    path('rate/<slug>/', views.RatingAPIView.as_view(), name='rating'),
    path('articles/<pk>/like/', views.LikeViewSet.as_view(
        {"patch": "partial_update"}), name='like_article'),
    path('articles/<pk>/dislike/', views.DisLikeViewSet.as_view(
        {"patch": "partial_update"}), name='dislike_article'),
]
