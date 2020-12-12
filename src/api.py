import os
import requests

from django.core.exceptions import ValidationError

from loguru import logger


def get_coordinates(country: str, city: str) -> dict:
    """Возвращает кортеж широты и долготы выбранного города страны."""
    geocode_api_key = os.environ['GEOCODE_API_KEY']
    geocode_url_template = "https://geocoder.ls.hereapi.com/6.2/geocode.json"
    geocode_url_params = {
        'country': country,
        'city': city,
        'apiKey': geocode_api_key,
    }
    json_geocode_api = requests.get(geocode_url_template, params=geocode_url_params).json()
    print(json_geocode_api)
    response = json_geocode_api['Response']
    view = response['View']
    if not view:
        logger.trace(f'Координаты страны "{geocode_url_params["country"]}" и города "{geocode_url_params["city"]}" не найдены.')
        raise ValidationError(f'Координаты страны "{geocode_url_params["country"]}" и города "{geocode_url_params["city"]}" не найдены.')
    result = view[0]['Result'][0]
    location = result['Location']
    coordinates = location['DisplayPosition']
    return coordinates


def get_timezone(latitude, longitude) -> str:
    """Возвращает временную зону в формате GMT с учетом перевода времени.
    Ограничение - 20.000 запросов в день."""
    geonames_username = os.environ['GEONAMES_USERNAME']
    timezone_url_template = "http://api.geonames.org/timezoneJSON"
    timezone_url_params = {
        'lat': latitude,
        'lng': longitude,
        'username': geonames_username,
    }
    json_geonames_api = requests.get(timezone_url_template, params=timezone_url_params).json()
    timezone = json_geonames_api.get('timezoneId')
    return timezone
