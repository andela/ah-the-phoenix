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
    path('articles/<pk>/comments/', views.CommentViewSet.as_view(
        {'get': 'list', "post": "create"}), name='comments-all'),
    path('articles/<pk>/comments/<id>/', views.CommentViewSet.as_view(
        {'get': 'retrieve', "put": "update",
         "delete": "destroy", "post": "create_reply"}), name='single-comment'),
    path('favorites/', views.FavoriteViewSet.as_view({"get": "list"}),
         name='favorites'),
    path('articles/<slug>/favorite',
         views.FavoriteViewSet.as_view({
             "put": "update", "delete": "destroy"}), name="favorite_article"),
]
