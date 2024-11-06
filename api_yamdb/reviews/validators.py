from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(data):
    if data >= (now := timezone.now().year):
        raise ValidationError(
            f'{data} не может быть больше {now}.'
        )
