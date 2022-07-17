import datetime
from PIL import Image

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from main.validators import PhotoSizeValidator


def phone_validator(phone: str):
    if len(phone) != 11:
        raise ValidationError('Некорректная длина номера!')
    elif not phone.isdigit():
        raise ValidationError('Проверьте правильность набранного номера!')


class Customer(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    user = models.OneToOneField(
        User,
        on_delete=models.deletion.CASCADE,
        verbose_name='Пользователь'
    )
    name = models.CharField(
        max_length=64,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=64,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        verbose_name='Электронная почта'
    )
    phone = models.CharField(
        max_length=11,
        verbose_name='Телефон',
        validators=[phone_validator]
    )
    ...

    def __str__(self) -> str:
        return f'{self.name} {self.surname}'


class Comfortable(models.Model):
    class Meta:
        verbose_name = 'Дополнительное удобство'
        verbose_name_plural = 'Дополнительные удобства'

    name = models.CharField(
        max_length=64,
        verbose_name='Название'
    )
    description = models.CharField(
        max_length=128,
        verbose_name='Описание'
    )

    def __str__(self) -> str:
        return f'{self.name}'


class Room(models.Model):
    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    name = models.CharField(
        max_length=128,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='main/photos/',
        blank=True,
        validators=[PhotoSizeValidator]
    )
    city = models.CharField(
        max_length=64,
        verbose_name='Город'
    )
    address = models.CharField(
        max_length=256,
        verbose_name='Адрес'
    )
    comfortables = models.ManyToManyField(
        Comfortable,
        related_name='hotel_comfortables',
        verbose_name='Удобства',
        blank=True
    )
    luxe = models.BooleanField(
        verbose_name='Люкс',
        default=False
    )
    price = models.IntegerField(
        verbose_name='Цена'
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    wifi = models.BooleanField(
        verbose_name='Наличие Wi-Fi',
        default=False
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def __str__(self) -> str:
        return f'"{self.name}" по адресу {self.address}'


class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    author = models.ForeignKey(
        Customer,
        on_delete=models.deletion.CASCADE,
        related_name='customer_reviews'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.deletion.CASCADE,
        related_name='room_reviews'
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(
        verbose_name='Комментарий'
    )
    created = models.DateTimeField(
        verbose_name='Создано',
        auto_now_add=True
    )
    updated = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.id:
            self.updated = datetime.datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Отзыв "{self.author}" для {self.room} | {self.created.strftime("%d.%m.%Y %H:%M")}'