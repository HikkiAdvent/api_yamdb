from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, response, status, views
from rest_framework_simplejwt.tokens import AccessToken

from api.v1 import mixins
from api.v1.permissions import OnlyAdmin
from api.v1.users.serializers import (
    TokenObtainSerializer, UserRegistrationSerializer, UserSerializer
)
from api.v1.users.utils import send_confirmation_email

User = get_user_model()


class UserRegistrationView(views.APIView):
    """Регистрация пользователя и отправка кода подтверждения."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_confirmation_email(user)
            return response.Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TokenObtainView(views.APIView):
    """Получение JWT токена по коду подтверждения."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = AccessToken.for_user(user)
            return response.Response(
                {'token': str(token)},
                status=status.HTTP_200_OK
            )
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserListCreate(mixins.ListCreateMixin):
    """Получение списка пользователей или их создание."""

    queryset = User.objects.all()
    permission_classes = (OnlyAdmin,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)


class UserRetrieveUpdateDestroy(mixins.RetrieveUpdateDestroyMixin):
    """Получение, обновление или удаление пользователя."""

    queryset = User.objects.all()
    permission_classes = (OnlyAdmin,)
    serializer_class = UserSerializer
    lookup_field = 'username'


class UserRetrieveUpdate(mixins.RetrieveUpdateMixin):
    """Получение или обновление своего аккаунта."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(role=self.get_object().role)
