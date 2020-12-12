import os

from django.conf import settings
from django.core.mail import send_mail

from astrostori.celery import app
from settings.models import DefaultSettingsModel
from src.selenium import download_starmap, get_driver
from src.utils import delete_file_list, load_config_file, rotate_svg_image


@app.task()
def get_starmap_task(starmap_url: str, starmap_shade_galaxy: bool, hours: str, minutes: str,
                     client_order_id: str, force_download=False):
    """Ассинхронное выполнение для получения звездной карты и поворота на 180 градусов."""
    config_data = load_config_file()
    try:
        starmap_filename = config_data['starmap']['STARMAP_FILENAME']
    except KeyError:
        raise Exception(f'Конфигурационный файл {settings.CONFIG_FILE} не корректно настроен.')
    width = DefaultSettingsModel.objects.first().starmap_width
    height = DefaultSettingsModel.objects.first().starmap_height
    angle = DefaultSettingsModel.objects.first().starmap_angle
    image_directory = os.path.join(settings.BASE_DIR, 'media', 'clients', client_order_id)
    driver = get_driver(image_directory)
    os.makedirs(image_directory, exist_ok=True)
    image_path = os.path.join(image_directory, starmap_filename)
    flag_downloaded_starmap = False
    while force_download or starmap_filename not in os.listdir(image_directory):
        # Перезаписывается файл, если он существует
        try:
            os.remove(os.path.join(image_directory, starmap_filename))
        except FileNotFoundError:
            pass
        download_starmap(driver, starmap_url, starmap_shade_galaxy, hours, minutes, width, height)
        flag_downloaded_starmap = True
        force_download = False
    driver.close()
    delete_file_list(image_directory, file_type='.crdownload')
    if flag_downloaded_starmap:
        rotate_svg_image(image_path, angle)


# @app.task(bind=True)
# def send_mail_task(self, subject, message, send_from, email_list, countdown, max_retries):
#     """Отправляет письма списку email почт."""
#     try:
#         send_mail(subject, message, send_from, email_list, fail_silently=True)
#     except Exception as exception:
#         self.retry(exc=exception, countdown=countdown, max_retries=max_retries)
