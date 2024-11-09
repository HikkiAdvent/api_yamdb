from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.constants import ROLE_LENGTH


class MyUser(AbstractUser):
    """Кастомный пользователь."""

    class Role(models.TextChoices):
        """Список ролей пользователя с читаемыми названиями."""
        USER = "user", _("User")
        MODERATOR = "moderator", _("Moderator")
        ADMIN = "admin", _("Admin")

    email = models.EmailField(
        unique=True,
        verbose_name='почта'
    )
    role = models.CharField(
        max_length=ROLE_LENGTH,
        choices=Role.choices,
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
        max_length=8,
        unique=True,
        verbose_name='код'
    )
    created_at = models.DateTimeField(
        'время создания',
        auto_now_add=True
    )

    def __str__(self):
        return f'Код подтверждения для {self.user.username}: {self.code}'
