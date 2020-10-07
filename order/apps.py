from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'order'
    verbose_name = 'Звездная карта'

    def ready(self):
        """Подключение файла с сигналами."""
        import order.signals
