from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    """Проверка корректности указания года создания(исключаем будущее время)"""
    if value > datetime.now().year:
        raise ValidationError(
            ('Ошибка, проверьте год создания произведения!'),
            params={'value': value},)