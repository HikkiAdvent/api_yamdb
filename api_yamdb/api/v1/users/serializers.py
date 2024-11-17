from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators

from api.v1.constants import EMAIL_LENGTH, USERNAME_LENGTH
from api.v1.users.utils import check_confirmation_code
from api.v1.users.validators import username_validator

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Регистрация пользователей."""

    email = serializers.EmailField(max_length=EMAIL_LENGTH, required=True)
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        required=True,
        validators=(username_validator,)
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        existing_user = User.objects.filter(
            username=username,
            email=email
        ).first()
        if existing_user:
            self.instance = existing_user
            return data
        if User.objects.filter(username=username).exists():
            raise validators.ValidationError(
                'Пользователь с таким именем уже существует.'
            )
        if User.objects.filter(email=email).exists():
            raise validators.ValidationError(
                'Пользователь с такой электронной почтой уже существует.'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Данные пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
    read_only_fields = ('role',)


class TokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения JWT токена."""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=8, required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not check_confirmation_code(user, confirmation_code):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения.'}
            )
        data['user'] = user
        return data
