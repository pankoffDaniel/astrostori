from django.db import models


class OrderStatusModel(models.Model):
    """Модель статуса заказа."""
    status = models.CharField('Статус заказа', max_length=255, unique=True)

    def __str__(self):
        return self.status

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

    def __str__(self):
        return 'Настройки'

    class Meta:
        verbose_name = 'Настройка по умолчанию'
        verbose_name_plural = 'Настройки по умолчанию'
