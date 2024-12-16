from django.core.exceptions import ValidationError

# Список разрешенных моделей
allowed_robot_models = {
    'R2': ['D2', 'D3', 'D4', 'D5'],
    '13': ['XS', 'XR', 'XL', 'XM'],
    'X5': ['LT', 'LR', 'LS', 'LM'],
}


def validate_model(data):
    """
    Валидатор проверяющий передавалсь ли в форму корректная
    модель робота и её наличие в списке разрешенных.
    """
    if 'model' not in data:
        raise ValidationError('Передана некорректная модель робота')
    if data['model'] not in allowed_robot_models:
        raise ValidationError('Эта модель робота не разрешена')


def validate_version(data):
    """
    Валидатор проверяющий передавалсь ли в форму корректная
    версия робота и её наличие в списке модели.
    """
    if 'version' not in data:
        raise ValidationError('Передана некорректная модель робота')
    if data['version'] not in allowed_robot_models[data['model']]:
        raise ValidationError('Эта версия робота не разрешена')
