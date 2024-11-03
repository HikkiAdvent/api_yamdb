from django.urls import path, include
from .views import UserRegistrationView, TokenObtainView, UserViewSet


auth = [
    path('signup/', UserRegistrationView.as_view(), name='registration'),
    path('token/', TokenObtainView.as_view(), name='token'),
]

users = [
    path('users/', UserViewSet, name='users')
]

urlpatterns = [
    path('auth/', include(auth))
]
