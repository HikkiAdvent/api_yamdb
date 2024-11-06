import uuid

from users.constants import UUID_LENGTH


def generate_short_uuid() -> str:
    """Генерирует код для входа из 8 символов"""
    return str(uuid.uuid4())[:UUID_LENGTH]
