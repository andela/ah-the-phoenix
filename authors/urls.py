"""authors URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin

from authors.apps.articles.views import ArticleViewSet
from .swagger import schema_view
from rest_framework import routers

router = routers.DefaultRouter()
router.register('articles', ArticleViewSet, base_name='articles')


# app_name = 'articles'
urlpatterns = [
    path('api/v1/', include(('authors.apps.articles.urls',
                             'articles'), namespace='articles')),
    path('admin/', admin.site.urls),
    path('', include('authors.apps.base.urls')),
    path('api/v1/docs/', schema_view),
    path('api/v1/', include(('authors.apps.authentication.urls',
                             'authentication'), namespace='authentication')),
    path('api/v1/', include(('authors.apps.notify.urls',
                             'notify'), namespace='notifications'))
]
