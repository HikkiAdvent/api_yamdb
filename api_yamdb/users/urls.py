from django.urls import path, include
from .views import UserRegistrationView, TokenObtainView


auth = [
    path('signup/', UserRegistrationView.as_view(), name='registration'),
    path('token/', TokenObtainView.as_view(), name='token'),
]

urlpatterns = [
    path('auth/', include(auth))
]
