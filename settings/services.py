from settings.models import DefaultSettingsModel, OrderClientTypeModel, OrderStatusModel


def get_default_client_type():
    client_type = DefaultSettingsModel.objects.first().client_type
    return OrderClientTypeModel.objects.get(client_type=client_type).id


def get_default_order_status():
    order_status = DefaultSettingsModel.objects.first().order_status
    return OrderStatusModel.objects.get(order_status=order_status).id


def get_default_starmap_time():
    starmap_time = DefaultSettingsModel.objects.first().starmap_time
    return starmap_time
