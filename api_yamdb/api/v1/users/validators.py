from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def username_validator(value):
    symbol_validator = RegexValidator(
        regex=r'^[\w.@+-]+\Z',
        message='Имя пользователя может содержать'
                ' только буквы, цифры и @/./+/-/_.'
    )
    symbol_validator(value)
    if value.lower() == 'me':
        raise ValidationError(
            'Использование "me" в качестве имени пользователя запрещено.')
    return value
