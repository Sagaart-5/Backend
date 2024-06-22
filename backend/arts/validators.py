from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    year = timezone.now().year
    if value > year:
        raise ValidationError(
            f"Год создания не должен превышать текущий {year} год."
        )
