from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from settings.models import OrderStatusModel, OrderClientTypeModel, DefaultSettingsModel
from settings.services import get_default_client_type, get_default_order_status, get_default_starmap_time
from src import utils
from src.api import get_coordinates, get_timezone


class StarmapSizeModel(models.Model):
    """Модель размера звездной карты."""
    size = models.CharField('Размер звездной карты', max_length=255)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class StarmapTypeModel(models.Model):
    """Модель типа звездной карты."""
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
    client_type = models.ForeignKey(OrderClientTypeModel, on_delete=models.PROTECT, verbose_name='Тип клиента',
                                    default=get_default_client_type)

    # Заказ
    date = models.DateField('Дата звездного неба')
    country = models.CharField('Страна', max_length=255)
    city = models.CharField('Город', max_length=255)
    text = models.CharField('Текст', max_length=50)
    latitude = models.FloatField('Широта', blank=True, null=True,
                                 validators=[MinValueValidator(-90), MaxValueValidator(90)],
                                 help_text='От -90 до 90 включительно')
    longitude = models.FloatField('Долгота', blank=True, null=True,
                                  validators=[MinValueValidator(-180), MaxValueValidator(180)],
                                  help_text='От -180 до 180 включительно')
    additional_information = models.TextField('Дополнительная информация', blank=True)
    is_logo = models.BooleanField('Логотип', default=True)
    starmap_time = models.TimeField('Время звездного неба', default=get_default_starmap_time)
    starmap_type = models.ForeignKey(StarmapTypeModel, on_delete=models.PROTECT, verbose_name='Тип звездной карты')
    starmap_size = models.ForeignKey(StarmapSizeModel, on_delete=models.PROTECT, verbose_name='Размер звездной карты')
    order_status = models.ForeignKey(OrderStatusModel, on_delete=models.PROTECT, verbose_name='Статус',
                                     default=get_default_order_status)
    created_datetime = models.DateTimeField('Дата и время создания заказа', auto_now_add=True)
    changed_datetime = models.DateTimeField('Дата и время изменения заказа', auto_now=True)

    def __str__(self):
        return f'Клиентский заказ №{str(self.id)}'

    def validate_timezone_by_coordinates(self):
        """Проверяет временную зону по координатам."""
        timezone = get_timezone(self.latitude, self.longitude)
        if not timezone:
            self.validation_error_dict['latitude'] = 'Не определена временная зона введенных координат.'
            self.validation_error_dict['longitude'] = 'Не определена временная зона введенных координат.'

    def validate_country_and_city(self):
        """Проверяет страну и город."""
        try:
            get_coordinates(self.country, self.city)
        except ValidationError:
            if StarmapOrderModel.objects.filter(pk=self.id).exists():
                self.validation_error_dict['country'] = 'Координаты не найдены.'
                self.validation_error_dict['city'] = 'Координаты не найдены.'

    def validate_coordinates(self):
        """Проверяет координаты."""
        latitude = isinstance(self.latitude, float)
        longitude = isinstance(self.longitude, float)
        if latitude and longitude:
            self.validate_timezone_by_coordinates()
        elif longitude and not latitude:
            self.validation_error_dict['latitude'] = 'Введите ширину.'
        elif latitude and not longitude:
            self.validation_error_dict['longitude'] = 'Введите долготу.'

    def clean(self):
        """Запускает дополнительные валидации полей страны, города, ширины и долготы."""
        self.validation_error_dict = {}
        self.validate_country_and_city()
        self.validate_coordinates()
        if self.validation_error_dict:
            raise ValidationError(self.validation_error_dict)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
