from django.contrib import admin

from settings.models import OrderClientTypeModel, DefaultSettingsModel, OrderStatusModel


@admin.register(OrderClientTypeModel)
class OrderClientTypeAdmin(admin.ModelAdmin):
    """Тип клиента в админке."""
    list_display = ('id', 'client_type')
    list_display_links = ('id', 'client_type')


@admin.register(DefaultSettingsModel)
class DefaultSettingsAdmin(admin.ModelAdmin):
    """Стандартные значения в админке."""
    list_display = ('id', 'client_type', 'order_status')
    list_display_links = ('id', 'client_type', 'order_status')

    def has_add_permission(self, request):
        """Можно добавить только одну запись."""
        return DefaultSettingsModel.objects.count() < 1


@admin.register(OrderStatusModel)
class OrderStatusAdmin(admin.ModelAdmin):
    """Статус заказа в админке."""
    list_display = ('id', 'status')
    list_display_links = ('id', 'status')
