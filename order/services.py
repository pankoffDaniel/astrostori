import os
import toml

from django.conf import settings
from django.http import HttpResponseBadRequest

from loguru import logger
from order.tasks import get_starmap_task
from src.api import get_coordinates, get_timezone
from src.utils import get_correct_date


def save_starmap(request: object):
    try:
        config_data = toml.load(settings.CONFIG_FILE_DIR)
        hours = config_data['starmap']['HOURS']
        minutes = config_data['starmap']['MINUTES']
        width = config_data['starmap']['WIDTH']
        height = config_data['starmap']['HEIGHT']
        angle = config_data['starmap']['ANGLE']
    except FileNotFoundError:
        raise Exception(
            f'Конфигурационный файл {settings.CONFIG_FILE} не найден.'
            f'Файл должен находиться по пути {settings.BASE_DIR}/{settings.CONFIG_FILE}')
    except KeyError:
        raise Exception(f'Конфигурационный файл {settings.CONFIG_FILE} не корректно настроен.')

    geocode_api_url = 'https://geocoder.ls.hereapi.com/6.2/geocode.json'
    geocode_api_key = os.environ['GEOCODE_API_KEY']

    date = request.get('date')
    year, month, day = get_correct_date(str(date), separate='-')
    additional_info = request.get('additional_info')
    set_logo = request.get('set_logo')
    latitude = request.get('altitude')
    longitude = request.get('longitude')

    country = request.get('country')
    city = request.get('city')
    params = {
        'country': country,
        'city': city,
        'gen': '9',
        'apiKey': geocode_api_key,
    }

    if not date or not country or not city:
        return HttpResponseBadRequest('400 Bad Request')

    if not latitude or not longitude:
        coordinates = get_coordinates(geocode_api_url, params)
        latitude = coordinates.get('Latitude')
        longitude = coordinates.get('Longitude')

    geonames_username = os.environ['GEONAMES_USERNAME']
    timezone = get_timezone(latitude, longitude, geonames_username)
    starmap_url = f'https://in-the-sky.org/skymap2.php?year={year}&month={month}&day={day}' \
                  f'&latitude={latitude}&longitude={longitude}&timezone={timezone}'
    image_name = 'sky_view.svg'

    logger.trace(f'{starmap_url} | logo - {set_logo} | description - {additional_info}', )
    get_starmap_task.delay(starmap_url, hours, minutes, width, height, angle, image_name,
                           client_order_id=str(request.get('id')), force_download=True)
