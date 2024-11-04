from django.shortcuts import get_object_or_404
from rest_framework import (
    permissions, status, views, response, generics, response
)
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import ConfirmationCode
from .serializers import (
    UserRegistrationSerializer, TokenObtainSerializer, UserSerializer
)
from users.uuids import generate_short_uuid
from .permissions import AdminPermission
User = get_user_model()


class UserRegistrationView(views.APIView):
    '''Регистрация новых пользователей.'''
    permission_classes = [permissions.AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            code, _ = ConfirmationCode.objects.update_or_create(
                user=user,
                defaults={
                    'code': generate_short_uuid(),
                    'created_at': timezone.now()
                }
            )
            if serializer.instance == user:
                send_mail(
                    'Код подтверждения',
                    f'Ваш код подтверждения: {code.code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                return response.Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {code.code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        print(serializer.errors)
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TokenObtainView(views.APIView):
    '''Получение токена по коду'''
    permission_classes = [permissions.AllowAny,]

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
    queryset = User.objects.all()
    permission_classes = (AdminPermission,)
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (AdminPermission,)
    serializer_class = UserSerializer

    def get_object(self):
        """Получение пользователя по username вместо id."""
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)


class UserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def put(self, request, *args, **kwargs):
        return response.Response(
            {"detail": "Метод PUT не разрешен."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
