from django.urls import include, path

app_name = 'api'


urlpatterns = [
    path('v1/', include('api.v1.urls'))
]

"Это надо перенести внутрь api/v1, так как это 1-я версия api"
# from rest_framework.routers import DefaultRouter

# from api import views


# router = DefaultRouter()
# router.register(
#     r'titles/(?P<title_id>\d+/reviews)',
#     views.ReviewViewSet,
#     basename='review')
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     views.CommentViewSet,
#     basename='comment')

# api_v1 = [
#     path('', include(router.urls)),
#     path('', include('users.urls'))
# ]

# urlpatterns = [
#     path('v1/', include(api_v1))
# ]
