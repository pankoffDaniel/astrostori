import os

from django.contrib import admin
from django.utils.safestring import mark_safe

from src.utils import load_config_file
from .models import StarmapModel, StarmapOrderModel, StarmapSizeModel


@admin.register(StarmapSizeModel)
class StarmapSizeAdmin(admin.ModelAdmin):
    """Размер звездной карты в формате 30x50 (ширина|высота) в админке."""
    list_display = ('id', 'size')
    list_display_links = ('id', 'size')


@admin.register(StarmapModel)
class StarmapAdmin(admin.ModelAdmin):
    """Шаблон заказа звездной карты в админке."""
    list_display = ('id', 'title', 'get_image', 'shade_galaxy')
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
    # TODO: сделать раскрывающийся инлайн с данными заказа (заказ один, но много картин можно добавлять)
    list_display = ('id', 'name', 'email', 'phone_number', 'date', 'is_image')
    list_display_links = ('id', 'name', 'email', 'phone_number', 'date')
    readonly_fields = ('created_datetime', 'changed_datetime', 'get_image')
    save_as = True
    save_on_top = True
    fieldsets = (
        ('Персональные данные', {
            'fields': (
                'name', 'email', 'phone_number', 'address', 'additional_information',
            )
        }),
        ('Данные заказа', {
            'fields': (
                'country', 'city',
                'date', 'text',
                ('starmap_type', 'starmap_size'),
                'is_logo', 'created_datetime', 'changed_datetime',
                'get_image',
            )
        }),
    )

    def has_delete_permission(self, request, obj=None):
        """Право на удаление есть только у супер-пользователя."""
        if request.user.is_superuser:
            return True
        return False

    def is_image(self, obj):
        """Отображение миниатюры полученной зездной карты."""
        config_data = load_config_file()
        starmap_filename = config_data['starmap']['STARMAP_FILENAME']
        starmap_directory = os.path.join('media', 'clients', str(obj.id))
        if not os.path.exists(starmap_directory) or starmap_filename not in os.listdir(starmap_directory):
            return '-'
        return '+'

    # TODO: не нравятся пути в таком виде
    def get_image(self, obj):
        """Отображение миниатюры полученной зездной карты."""
        config_data = load_config_file()
        starmap_filename = config_data['starmap']['STARMAP_FILENAME']
        starmap_directory = os.path.join('media', 'clients', str(obj.id))
        if not os.path.exists(starmap_directory) or starmap_filename not in os.listdir(starmap_directory):
            return 'Нет изображения'
        return mark_safe(
            f'<a href="{os.path.join("/media", "clients", str(obj.id), starmap_filename)}" target="_blank">'
            f'<img src="{os.path.join("/media", "clients", str(obj.id), starmap_filename)}" width="100" height="100">'
            f'</a>')

    get_image.short_description = 'Изображение'
    is_image.short_description = 'Есть изображение'


# Настройка названия админки сайта
# TODO: каждая роль персонала отмечается цветом и настроить права доступа
admin.site.site_header = 'ASTROSTORI'
admin.site.site_title = 'ASTROSTORI'
