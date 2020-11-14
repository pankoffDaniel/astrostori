import requests
from django.core.exceptions import ValidationError
from loguru import logger


def get_coordinates(geocode_api_url: str, params: dict) -> dict:
    """Возвращает кортеж широты и долготы выбранного города страны."""
    # TODO: вынести в функцию получение ответа API
    # TODO: выводить message.error
    json_geocode_api = requests.get(geocode_api_url, params=params).json()
    print(json_geocode_api)
    response = json_geocode_api['Response']
    view = response['View']
    if not view:
        logger.trace(f'Координаты страны "{params["country"]}" и города "{params["city"]}" были не найдены.')
        raise ValidationError(f'Координаты страны "{params["country"]}" и города "{params["city"]}" были не найдены.')
    result = view[0]['Result'][0]
    location = result['Location']
    coordinates = location['DisplayPosition']
    return coordinates


def get_timezone(latitude: str, longitude: str, geonames_username: str) -> str:
    """Возвращает временную зону в формате GMT с учетом перевода времени.
    Ограничение - 20.000 запросов в день."""
    timezone_url = f"http://api.geonames.org/timezoneJSON?lat={latitude}&lng={longitude}&username={geonames_username}"
    json_geonames_api = requests.get(timezone_url).json()
    timezone = json_geonames_api.get('timezoneId')
    return timezone
