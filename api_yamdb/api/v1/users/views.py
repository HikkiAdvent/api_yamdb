from api.v1.users.mixins import NoPutAPIViewMixin
from api.v1.users.permissions import AdminPermission
from api.v1.users.serializers import (TokenObtainSerializer,
                                      UserRegistrationSerializer,
                                      UserSerializer)
from api.v1.users.uuids import generate_short_uuid, send_confirmation_code
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import (filters, generics, permissions, response, status,
                            views)
from rest_framework_simplejwt.tokens import AccessToken

from users.models import ConfirmationCode

User = get_user_model()


class UserRegistrationView(views.APIView):
    """Регистрация новых пользователей."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user, created = User.objects.get_or_create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                defaults={'username': serializer.validated_data['username']}
            )
            code, _ = ConfirmationCode.objects.update_or_create(
                user=user,
                defaults={
                    'code': generate_short_uuid(),
                    'created_at': timezone.now()
                }
            )
            send_confirmation_code(user, code.code)
            return response.Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TokenObtainView(views.APIView):
    """Получение токена по коду."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
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


class UserListCreate(generics.ListCreateAPIView):
    """Получение списка пользователей или их создание."""

    queryset = User.objects.all()
    permission_classes = (AdminPermission,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)


class UserRetrieveUpdateDestroy(
    NoPutAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """Получение, обновление или удаление пользователя."""

    queryset = User.objects.all()
    permission_classes = (AdminPermission,)
    serializer_class = UserSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)


class UserRetrieveUpdate(NoPutAPIViewMixin, generics.RetrieveUpdateAPIView):
    """Получение или обновление своего аккаунта."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
