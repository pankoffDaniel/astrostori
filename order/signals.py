from django.db.models.signals import post_save
from django.dispatch import receiver

from order import services

from .models import StarmapOrderModel


@receiver(post_save, sender=StarmapOrderModel)
def create_client_starmap(sender, instance=None, **kwargs):
    """После сохранения заказа запускает процесс получения карты
    и передает все данные сохранения."""
    services.save_starmap(instance.__dict__)
