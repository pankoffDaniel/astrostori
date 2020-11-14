from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from src import utils
from src.api import get_coordinates


class StarmapSizeModel(models.Model):
    """Модель размера звездной карты в формате 30x50 (ширина и высота)."""
    size = models.CharField('Размер звездной карты', max_length=255)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class StarmapModel(models.Model):
    """Модель шаблона заказа звездной карты."""
    title = models.CharField('Название звездной карты', max_length=255)
    image = models.ImageField('Изображение', upload_to=utils.get_starmap_image_upload_path_in_catalog)
    shade_galaxy = models.BooleanField('Сияние', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class StarmapOrderModel(models.Model):
    """Модель заказа звездной карты."""
    # Персональные данные
    name = models.CharField('Имя', max_length=255)
    email = models.EmailField('Email')
    address = models.CharField('Адресс', max_length=255)
    phone_number = models.CharField('Номер телефона', max_length=255)

    # Заказ
    date = models.DateField('Дата')
    country = models.CharField('Страна', max_length=255)
    city = models.CharField('Город', max_length=255)
    text = models.CharField('Текст', max_length=50)
    latitude = models.FloatField('Широта', blank=True, null=True,
                                 validators=[MinValueValidator(-90), MaxValueValidator(90)],
                                 help_text='Если вводите широту, то и долготу тоже. Пример: 55.75697')
    longitude = models.FloatField('Долгота', blank=True, null=True,
                                  validators=[MinValueValidator(-180), MaxValueValidator(180)],
                                  help_text='Если вводите долготу, то и ширину тоже. Пример: 37.61502')
    additional_information = models.TextField('Дополнительная информация', blank=True)
    is_logo = models.BooleanField('Логотип', default=True)
    starmap_type = models.ForeignKey(StarmapModel, on_delete=models.PROTECT, verbose_name='Тип звездной карты')
    starmap_size = models.ForeignKey(StarmapSizeModel, on_delete=models.PROTECT, verbose_name='Размер звездной карты')
    created_datetime = models.DateTimeField('Дата и время создания заказа', auto_now_add=True)
    changed_datetime = models.DateTimeField('Дата и время изменения заказа', auto_now=True)

    def __str__(self):
        return f'Клиентский заказ №{str(self.id)}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
