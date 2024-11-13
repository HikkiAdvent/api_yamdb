from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail


def generate_confirmation_code(user):
    """Генерация кода подтверждения."""

    return default_token_generator.make_token(user)


def check_confirmation_code(user, token):
    """Проверка кода подтверждения."""

    return default_token_generator.check_token(user, token)


def send_confirmation_email(user):
    token = generate_confirmation_code(user)
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {token}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
