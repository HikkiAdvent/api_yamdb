import uuid

from users.constants import UUID_LENGTH


def generate_short_uuid():
    '''Генерирует укороченный UUID из первых 8 символов'''
    return str(uuid.uuid4())[:UUID_LENGTH]
