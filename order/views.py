import traceback

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from loguru import logger
from order import services


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
    services.save_starmap(request.POST)
    return HttpResponse('200 OK')
