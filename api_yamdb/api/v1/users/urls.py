from django.urls import include, path

from api.v1.users import views

auth = [
    path('signup/', views.UserRegistrationView.as_view(), name='registration'),
    path('token/', views.TokenObtainView.as_view(), name='token'),
]

users = [
    path(
        'me/',
        views.UserRetrieveUpdate.as_view(
            {'get': 'retrieve', 'patch': 'partial_update'}
        ),
        name='me'
    ),
    path(
        '<username>/',
        views.UserRetrieveUpdateDestroy.as_view(
            {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}
        ),
        name='user'
    ),
    path(
        '',
        views.UserListCreate.as_view(
            {'get': 'list', 'post': 'create'}
        ),
        name='users'
    ),
]

urlpatterns = [
    path('auth/', include(auth)),
    path('users/', include(users))
]
