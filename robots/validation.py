from django.core.exceptions import ValidationError

# Список разрешенных моделей
allowed_robot_models = {
    'R2': ['D2'],
    '13': ['XS'],
    'X5': ['LT'],
}


def validate_model(data):
    """
    Валидатор проверяет наличие
    модели робота в списке разрешенных.
    """
    if 'model' not in data:
        raise ValidationError('Передана некорректная модель робота')
    if data['model'] not in allowed_robot_models:
        raise ValidationError('Эта модель робота не разрешена')
