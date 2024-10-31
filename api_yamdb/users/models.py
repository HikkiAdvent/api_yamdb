from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    admin = models.BooleanField(default=False)


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
