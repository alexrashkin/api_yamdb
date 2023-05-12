from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка корректности указания года создания произведения"""
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f"Год создания произведения не может быть больше {current_year}."
        )