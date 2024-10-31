from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import ConfirmationCode

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Использование 'me' в качестве имени пользователя запрещено."
            )
        return value


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=8)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

        if not ConfirmationCode.objects.filter(
            user=user,
            code=confirmation_code
        ).exists():
            raise serializers.ValidationError("Неверный код подтверждения.")
        data['user'] = user
        return data
