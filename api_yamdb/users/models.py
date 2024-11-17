from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.constants import ROLE_LENGTH


class MyUser(AbstractUser):
    """Кастомный пользователь."""

    class Role(models.TextChoices):
        """Список ролей пользователя."""

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
        verbose_name='роль'
    )
    bio = models.TextField(
        blank=True,
        default='',
        verbose_name='биография'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'password')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def clean(self) -> None:
        if self.username == 'me':
            raise ValidationError('Имя пользователя не может быть "me"')
        return super().clean()

    @property
    def is_moderator_or_admin(self) -> bool:
        return (
            self.role in (self.Role.MODERATOR, self.Role.ADMIN)
            or self.is_superuser
        )

    @property
    def is_admin(self) -> bool:
        return (
            self.role == self.Role.ADMIN
            or self.is_superuser
        )
