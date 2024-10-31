from django.urls import include, path
from rest_framework import DefaultRouter
from . import views

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+/reviews)',
    views.ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
]
