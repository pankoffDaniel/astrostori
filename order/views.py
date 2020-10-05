import os
import toml
import traceback

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from loguru import logger
from src.api import get_coordinates, get_timezone
from src.utils import get_correct_date
from order.tasks import get_starmap


logger.add('logs/trace.log', format='{time:DD:MM:YY HH:mm:ss} {level} {message}', level='TRACE')


def json_response(json_object, status=200):
    """Возвращает JSON ответ."""
    return JsonResponse(json_object, status=status, safe=True)


def error_response(exception):
    """Форматирует HTTP ответ с описанием ошибки и Traceback."""
    response = {'traceback': traceback.format_exc()}
    logger.trace(response['traceback'])
    if settings.DEBUG:
        return json_response(response, status=500)
    return HttpResponseBadRequest('500 Server Error')


def base_view(view):
    """Декоратор для всех вьюшек и обрабатывает все исключения."""
    def wrapper(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except Exception as exception:
            return error_response(exception)
    return wrapper


def form(request):
    return render(request, 'order/form.html')


@csrf_exempt
@base_view
def get_order(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('400 Bad Request')
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

    agreement = request.POST.get('agreement')
    if not agreement:
        return HttpResponseBadRequest()

    geocode_api_url = 'https://geocoder.ls.hereapi.com/6.2/geocode.json'
    geocode_api_key = os.environ['GEOCODE_API_KEY']

    date = request.POST.get('date')
    year, month, day = get_correct_date(date)
    additional_info = request.POST.get('additional_info')
    set_logo = request.POST.get('set_logo')
    latitude = request.POST.get('altitude')
    longitude = request.POST.get('longitude')

    country = request.POST.get('country')
    city = request.POST.get('city')
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
    get_starmap.delay(starmap_url, hours, minutes, width, height, angle, image_name, force_download=False)
    return HttpResponse('200 OK')
