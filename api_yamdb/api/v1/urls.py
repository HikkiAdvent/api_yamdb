from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1 import views


router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('titles', views.TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+/reviews)', views.ReviewViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment')


urlpatterns = [
    path('', include('users.urls')),
    path('', include(router.urls))
]
