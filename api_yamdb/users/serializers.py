from django.http import Http404
from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from users.models import ConfirmationCode

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message=(
                    'Имя пользователя может содержать'
                    ' только буквы, цифры и @/./+/-/_.'
                )
            )
        ]
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
                "Пользователь с таким именем уже существует."
            )
        if User.objects.filter(email=email).exists():
            raise validators.ValidationError(
                "Пользователь с такой электронной почтой уже существует."
            )
        return data

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Использование 'me' в качестве имени пользователя запрещено."
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=8)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("Пользователь не найден.")
        if not ConfirmationCode.objects.filter(
            user=user,
            code=confirmation_code
        ).exists():
            raise serializers.ValidationError("Неверный код подтверждения.")
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
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
