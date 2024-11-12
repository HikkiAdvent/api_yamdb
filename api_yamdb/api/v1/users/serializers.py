from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.http import Http404
from rest_framework import serializers, validators

from api.v1.users.constants import EMAIL_LENGTH, USERNAME_LENGTH
from .validators import username_validator
from users.models import ConfirmationCode

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

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenObtainSerializer(serializers.Serializer):
    """Проверка токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=8)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404('Пользователь не найден.')
        if not ConfirmationCode.objects.filter(
            user=user,
            code=confirmation_code
        ).exists():
            raise serializers.ValidationError('Неверный код подтверждения.')
        data['user'] = user
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
            'role'
        )

    def update(self, instance, validated_data):
        if not (
            self.context['request'].user.is_superuser
            and self.context['request'].user.role != User.Role.ADMIN
        ):
            validated_data.pop('role', None)
        return super().update(instance, validated_data)
