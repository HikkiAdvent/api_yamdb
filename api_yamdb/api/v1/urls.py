from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet)

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

auth_urls = [
...
]


urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(router.urls))
]
