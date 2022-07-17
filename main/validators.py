from django.core.exceptions import ValidationError


def PhotoSizeValidator(photo):
    max_size_mb = 2
    if photo.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Слишком большой размер файла! (макс. {max_size_mb} мб)")