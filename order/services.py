import os

from django.conf import settings
from django.http import HttpResponseBadRequest

from .models import StarmapModel

from loguru import logger
from order.tasks import get_starmap_task
from src.api import get_coordinates, get_timezone
from src.utils import get_correct_date, load_config_file


def save_starmap(request: object):
    # TODO: принимать верные данные и правильно логгировать
    config_data = load_config_file()
    try:
        hours = config_data['starmap']['HOURS']
        minutes = config_data['starmap']['MINUTES']
        width = config_data['starmap']['WIDTH']
        height = config_data['starmap']['HEIGHT']
        angle = config_data['starmap']['ANGLE']
        starmap_filename = config_data['starmap']['STARMAP_FILENAME']
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

    # Получение булева значения для отображения сияния на звездной карте
    starmap_type_id = request.get('starmap_type_id')
    starmap_type = StarmapModel.objects.get(pk=starmap_type_id)
    starmap_shade_galaxy = starmap_type.shade_galaxy

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

    logger.trace(f'{starmap_url} | logo - {set_logo} | description - {additional_info}', )
    if timezone:
        get_starmap_task.delay(starmap_url, starmap_shade_galaxy, hours, minutes, width, height, angle, starmap_filename,
                               client_order_id=str(request.get('id')), force_download=True)
