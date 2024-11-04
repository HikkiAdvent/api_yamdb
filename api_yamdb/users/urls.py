from django.urls import path, include
from users import views


auth = [
    path('signup/', views.UserRegistrationView.as_view(), name='registration'),
    path('token/', views.TokenObtainView.as_view(), name='token'),
]

users = [
    path('', views.UserListCreate.as_view(), name='users'),
    path(
        '<username>/',
        views.UserRetrieveUpdateDestroy.as_view(),
        name='user'
    ),
    path('me/', views.UserRetrieveUpdate.as_view(), name='me')
]

urlpatterns = [
    path('auth/', include(auth)),
    path('users/', include(users))
]
