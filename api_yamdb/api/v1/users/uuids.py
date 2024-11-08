import uuid

from django.core.mail import send_mail
from django.conf import settings

from api.v1.users.constants import UUID_LENGTH


def generate_short_uuid() -> str:
    """Генерирует код для входа из 8 символов."""

    return str(uuid.uuid4())[:UUID_LENGTH]


def send_confirmation_code(user, code):
    """Отправка кода подтверждения пользователю."""

    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
