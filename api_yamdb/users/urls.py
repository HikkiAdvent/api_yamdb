from django.urls import path, include
from .views import UserRegistrationView, TokenObtainView


auth = [
    path('auth/signup/', UserRegistrationView.as_view(), name='registration'),
    path('auth/token/', TokenObtainView.as_view(), name='token'),
]

urlpatterns = [
    path('v1/', include(auth))
]
