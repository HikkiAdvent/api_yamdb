from rest_framework import permissions, status, views, response, viewsets
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import ConfirmationCode
from .serializers import UserRegistrationSerializer, TokenObtainSerializer, UserSerializer
from users.uuids import generate_short_uuid
from .permissions import AdminPermission
User = get_user_model()


class UserRegistrationView(views.APIView):
    '''Регистрация новых пользователей.'''
    permission_classes = [permissions.AllowAny,]

    def post(self, request, *args, **kwargs):
        '''
        Отправляет новый код или обновляет старый
        при повторной отправке данных.
        '''
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user, _ = User.objects.get_or_create(**serializer.validated_data)
            code, _ = ConfirmationCode.objects.update_or_create(
                user=user,
                defaults={
                    'code': generate_short_uuid(),
                    'created_at': timezone.now()
                }
            )
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {code.code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return response.Response(
                {
                    'message': 'Код отправлен на указанный email.'
                },
                status=status.HTTP_200_OK
            )
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AdminPermission,)
    serializer_class = UserSerializer
