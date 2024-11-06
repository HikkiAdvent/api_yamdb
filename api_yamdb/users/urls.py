from django.urls import include, path

from users import views

auth = [
    path('signup/', views.UserRegistrationView.as_view(), name='registration'),
    path('token/', views.TokenObtainView.as_view(), name='token'),
]

users = [
    path('me/', views.UserRetrieveUpdate.as_view(), name='me'),
    path(
        '<username>/',
        views.UserRetrieveUpdateDestroy.as_view(),
        name='user'
    ),
    path('', views.UserListCreate.as_view(), name='users'),
]

urlpatterns = [
    path('auth/', include(auth)),
    path('users/', include(users))
]
