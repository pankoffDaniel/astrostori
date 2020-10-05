import os

from django.conf import settings

from astrostori.celery import app
from src.selenium import download_starmap, get_driver
from src.utils import rotate_svg_image, delete_file_list


@app.task()
def get_starmap(starmap_url: str, hours: str, minutes: str, width: str, height: str, angle: str,
                image_name: str, force_download=False):
    """Ассинхронное выполнение для получения звездной карты и поворота на 180 градусов."""
    driver = get_driver()
    image_directory = os.path.join(settings.BASE_DIR, 'media')
    image_path = os.path.join(image_directory, image_name)
    flag_downloaded_starmap = False
    while force_download or image_name not in os.listdir(image_directory):
        download_starmap(driver, starmap_url, hours, minutes, width, height)
        flag_downloaded_starmap = True
        force_download = False
    driver.close()
    delete_file_list(image_directory, file_type='.crdownload')
    if flag_downloaded_starmap:
        rotate_svg_image(image_path, angle)
