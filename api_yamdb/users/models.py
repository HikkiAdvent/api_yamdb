from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class MyUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    role = models.CharField(
        max_length=20,
        choices=[(role.value, role.name) for role in Role],
        default=Role.USER.value,
        blank=True
    )
    bio = models.TextField(blank=True, null=True)


class ConfirmationCode(models.Model):
    user = models.OneToOneField(
        MyUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code'
    )
    code = models.CharField(
        max_length=8,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Код подтверждения для {self.user.username}: {self.code}'
