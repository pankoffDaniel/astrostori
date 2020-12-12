from django.db import models


class OrderStatusModel(models.Model):
    """Модель статуса заказа."""
    order_status = models.CharField('Статус заказа', max_length=255, unique=True)

    def __str__(self):
        return self.order_status

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class OrderClientTypeModel(models.Model):
    """Модель типа клиента."""
    client_type = models.CharField('Тип клиента', max_length=255, unique=True)

    def __str__(self):
        return self.client_type

    class Meta:
        verbose_name = 'Тип клиента'
        verbose_name_plural = 'Типы клиентов'


class DefaultSettingsModel(models.Model):
    """Модель стандартных значений."""
    client_type = models.ForeignKey(OrderClientTypeModel, on_delete=models.PROTECT,
                                    verbose_name='Стандартный тип клиента')
    order_status = models.ForeignKey(OrderStatusModel, on_delete=models.PROTECT,
                                     verbose_name='Стандартный статус заказа')
    starmap_time = models.TimeField('Время звездного неба', help_text='Вводить в формате 18:20')
    starmap_width = models.PositiveSmallIntegerField('Ширина звездной карты', help_text='В пикселях')
    starmap_height = models.PositiveSmallIntegerField('Высота звездной карты', help_text='В пикселях')
    starmap_angle = models.PositiveSmallIntegerField('Угол поворота звездной карты', help_text='В градусах')

    def __str__(self):
        return 'Настройки'

    class Meta:
        verbose_name = 'Настройка по умолчанию'
        verbose_name_plural = 'Настройки по умолчанию'
