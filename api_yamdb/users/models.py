from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

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
        verbose_name='роль'
    )
    bio = models.TextField(
        blank=True,
        default='',
        verbose_name='биография'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self) -> None:
        if self.username == 'me':
            raise ValidationError('Имя пользователя не может быть "me"')
        return super().clean()

    @property
    def is_moderator_or_admin(self) -> bool:
        return (
            self.role in {self.Role.MODERATOR, self.Role.ADMIN}
            or self.is_superuser
        )

    @property
    def is_admin(self) -> bool:
        return (
            self.role == self.Role.ADMIN
            or self.is_superuser
        )


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
