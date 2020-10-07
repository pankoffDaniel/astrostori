from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import StarmapModel, StarmapOrderModel


@admin.register(StarmapModel)
class StarmapAdmin(admin.ModelAdmin):
    """Шаблон заказа звездной карты в админке."""
    list_display = ('id', 'title', 'get_image')
    list_display_links = ('id', 'title')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<a href="{obj.image.url}" target="_blank">'
                             f'<img src="{obj.image.url}" width="100">'
                             f'</a>')
        return 'Нет изображения'

    def has_delete_permission(self, request, obj=None):
        """Право на удаление есть только у супер-пользователя."""
        if request.user.is_superuser:
            return True
        return False

    get_image.short_description = 'Миниатюра'


@admin.register(StarmapOrderModel)
class StarmapOrderAdmin(admin.ModelAdmin):
    """Заказ звездной карты в админке."""
    # TODO: сделать раскрывающийся инлайн с данными заказа
    list_display = ('id', 'name', 'email', 'phone_number', 'date', 'get_image')
    list_display_links = ('id', 'name', 'email', 'phone_number', 'date')
    readonly_fields = ('created_datetime', 'changed_datetime', 'get_image')
    fieldsets = (
        ('Персональные данные', {
            'fields': (
                'name', 'email', 'phone_number', 'address',
            )
        }),
        ('Данные заказа', {
            'fields': (
                'country', 'city',
                'date', 'text',
                'starmap_type', 'additional_information', 'is_logo',
                'created_datetime', 'changed_datetime',
                'get_image',
            )
        }),
    )

    def has_delete_permission(self, request, obj=None):
        """Право на удаление есть только у супер-пользователя."""
        if request.user.is_superuser:
            return True
        return False

    # TODO: не работает
    def get_image(self, obj):
        if obj.starmap_image:
            return mark_safe(f'<a href="{obj.starmap_image.url}" target="_blank">'
                             f'<img src="{obj.starmap_image.url}" width="100">'
                             f'</a>')
        return 'Нет изображения'

    get_image.short_description = 'Изображение'


# Настройка названия админки сайта
# TODO: каждая роль персонала отмечается цветом и настроить права доступа
admin.site.site_header = 'ASTROSTORI'
admin.site.site_title = 'ASTROSTORI'
