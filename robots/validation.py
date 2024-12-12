from django.core.exceptions import ValidationError

# Список разрешенных моделей
allowed_robot_models = {
    'R2': ['D2'],
    '13': ['XS'],
    'X5': ['LT'],
}


def validate_model(model):
    """Функция проверяющая входит ли модель в список разрешенных."""
    if model not in allowed_robot_models:
        raise ValidationError('This model is not allowed')
