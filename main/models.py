from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def phone_validator(phone: str):
    if len(phone) != 11:
        raise ValidationError('Некорректная длина номера!')
    elif not phone.isdigit():
        raise ValidationError('Проверьте правильность набранного номера!')


class Customer(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    user = models.OneToOneField(User, on_delete=models.deletion.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=64, verbose_name='Имя')
    surname = models.CharField(max_length=64, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(max_length=11, verbose_name='Телефон', validators=[phone_validator])
    ...

    def __str__(self) -> str:
        return f'{self.name} {self.surname}'


class Comfortable(models.Model):
    class Meta:
        verbose_name = 'Дополнительное удобство'
        verbose_name_plural = 'Дополнительные удобства'

    name = models.CharField(max_length=64, verbose_name='Название')
    description = models.CharField(max_length=128, verbose_name='Описание')

    def __str__(self) -> str:
        return f'{self.name}'


class Room(models.Model):
    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    name = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    city = models.CharField(max_length=64, verbose_name='Город')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    comfortables = models.ManyToManyField(Comfortable, related_name='hotel_comfortables', verbose_name='Удобства')
    price = models.IntegerField(verbose_name='Цена')
    wifi = models.BooleanField(verbose_name='Наличие Wi-Fi', default=False)
    ...

    def __str__(self) -> str:
        return f'"{self.name}" по адресу {self.address}'
