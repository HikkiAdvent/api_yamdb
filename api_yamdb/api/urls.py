from django.urls import include, path
from rest_framework import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
]