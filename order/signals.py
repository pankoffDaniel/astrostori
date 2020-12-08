from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import services

from .models import StarmapOrderModel
from .tasks import send_mail_task


@receiver(post_save, sender=StarmapOrderModel)
def create_client_starmap(sender, instance=None, **kwargs):
    """Email оповещение клиента и админа о новом заказе."""
    # TODO: сделать оформление email письма
    services.save_starmap(instance.__dict__)
    if kwargs.get('created'):
        # Оповещение клиента
        subject = 'Мы получили заказ'
        message = f'Скоро с Вами свяжется менеджер.' \
                  f'ID заказа: {instance.id}'
        send_from = settings.EMAIL_HOST_USER
        email_list = [instance.email]
        send_mail_task.delay(subject, message, send_from, email_list, countdown=5*60, max_retries=3)

        # Оповещение админа
        subject = 'Новый заказ'
        message = f'ID заказа: {instance.id}'
        send_from = settings.EMAIL_HOST_USER
        email_list = [settings.EMAIL_HOST_USER]
        send_mail_task.delay(subject, message, send_from, email_list, countdown=5*60, max_retries=3)
