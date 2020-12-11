from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest

from .models import StarmapOrderModel, StarmapTypeModel
from loguru import logger
from order.tasks import get_starmap_task
from src.api import get_coordinates, get_timezone
from src.utils import get_correct_date


def save_starmap(request):
    """Сохраняет звездную карту."""
    date = request.get('date')
    year, month, day = get_correct_date(str(date), separate='-')
    additional_information = request.get('additional_information')
    is_logo = True if request.get('is_logo') == 'on' else False
    latitude = request.get('latitude')
    longitude = request.get('longitude')
    country = request.get('country')
    city = request.get('city')
    starmap_type_id = request.get('starmap_type_id')
    starmap_type = StarmapTypeModel.objects.get(pk=starmap_type_id)

    # Получение булева значения для отображения сияния на звездной карте
    starmap_shade_galaxy = starmap_type.shade_galaxy

    if not date or not country or not city:
        return HttpResponseBadRequest('400 Bad Request')

    if latitude is None or longitude is None:
        # Если это новый заказ, то сохраняет его несмотря на
        # ненайденную пару страны и города для получения координат,
        # но не скачивает карту и остается статус "Нет изображения"
        try:
            coordinates = get_coordinates(country, city)
            latitude = coordinates.get('Latitude')
            longitude = coordinates.get('Longitude')
        except ValidationError:
            return

    timezone = get_timezone(latitude, longitude)
    starmap_url = f'https://in-the-sky.org/skymap2.php?year={year}&month={month}&day={day}' \
                  f'&latitude={latitude}&longitude={longitude}&timezone={timezone}'

    client_order_id = request.get('id')
    print('ID заказа:', client_order_id)
    logger.trace(f'id - {client_order_id} | {starmap_url} | logo - {is_logo} | description - {additional_information}')

    if timezone:
        get_starmap_task.delay(starmap_url, starmap_shade_galaxy,
                               client_order_id=str(client_order_id), force_download=True)


def create_order(request):
    """Создает заказ звездной карты (вызывается из вьюшки)."""
    name = request.get('name')
    email = request.get('email')
    address = request.get('address')
    phone_number = request.get('phone_number')
    date = request.get('date')
    text = request.get('text')
    additional_information = request.get('additional_information')
    is_logo = True if request.get('is_logo') == 'on' else False
    country = request.get('country')
    city = request.get('city')
    starmap_type_id = request.get('starmap_type_id')
    starmap_size_id = request.get('starmap_size_id')

    if not date or not country or not city:
        return HttpResponseBadRequest('400 Bad Request')

    StarmapOrderModel.objects.create(name=name, email=email, address=address, phone_number=phone_number, date=date,
                                     country=country, city=city, text=text,
                                     additional_information=additional_information, is_logo=is_logo,
                                     starmap_size_id=starmap_size_id, starmap_type_id=starmap_type_id)
