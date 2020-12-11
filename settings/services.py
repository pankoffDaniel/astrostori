from settings.models import DefaultSettingsModel


def get_default_client_type():
    client_type = DefaultSettingsModel.objects.first().client_type
    return client_type


def get_default_order_status():
    order_status = DefaultSettingsModel.objects.first().order_status
    return order_status
