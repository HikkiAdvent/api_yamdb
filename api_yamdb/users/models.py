from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import EMAIL_LENGTH, ROLE_LENGTH, CONFIRMATION_CODE_LENGTH


class MyUser(AbstractUser):
    """Кастомный пользователь."""

    class Role(models.TextChoices):
        """Список ролей."""
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(
        unique=True,
        max_length=EMAIL_LENGTH,
        verbose_name='почта'
    )
    role = models.CharField(
        max_length=ROLE_LENGTH,
        choices=[(role.value, role.name) for role in Role],
        default=Role.USER.value,
        blank=True,
        verbose_name='роль'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='биография'
    )

    class Meta:
        ordering = ('id',)


class ConfirmationCode(models.Model):
    """Код подтверждения."""

    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code'
    )
    code = models.CharField(
        max_length=CONFIRMATION_CODE_LENGTH,
        unique=True,
        verbose_name='код'
    )
    created_at = models.DateTimeField(
        'время создания',
        auto_now_add=True
    )

    def __str__(self):
        return f'Код подтверждения для {self.user.username}: {self.code}'
