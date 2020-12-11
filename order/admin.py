import os

from django.contrib import admin
from django.utils.safestring import mark_safe

from src.utils import load_config_file
from .models import StarmapOrderModel, StarmapTypeModel, StarmapSizeModel


@admin.register(StarmapSizeModel)
class StarmapSizeAdmin(admin.ModelAdmin):
    """Размер звездной карты в формате 30x50 (ширина и высота) в админке."""
    list_display = ('id', 'size')
    list_display_links = ('id', 'size')


@admin.register(StarmapTypeModel)
class StarmapTypeAdmin(admin.ModelAdmin):
    """Шаблон типа звездной карты в админке."""
    list_display = ('id', 'title', 'get_image', 'shade_galaxy')
    list_display_links = ('id', 'title')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<a href="{obj.image.url}" target="_blank">'
                             f'<img src="{obj.image.url}" width="100">'
                             f'</a>')
        return 'Нет изображения'
    get_image.short_description = 'Миниатюра'


@admin.register(StarmapOrderModel)
class StarmapOrderAdmin(admin.ModelAdmin):
    """Заказ звездной карты в админке."""
    list_display = ('id', 'name', 'email', 'phone_number', 'date', 'status', 'is_image')
    list_display_links = ('id', 'name', 'email', 'phone_number', 'date', 'status')
    readonly_fields = ('created_datetime', 'changed_datetime', 'get_image')
    save_as = True
    save_on_top = True
    fieldsets = (
        ('Персональные данные', {
            'fields': (
                'name', 'email', 'phone_number', 'address', 'client_type', 'additional_information',
            )
        }),
        ('Данные заказа', {
            'fields': (
                'country', 'city',
                'latitude', 'longitude',
                'date', 'text',
                ('starmap_type', 'starmap_size'),
                'is_logo', 'status', 'created_datetime', 'changed_datetime',
                'get_image',
            )
        }),
    )

    def is_image(self, obj):
        """Возвращает есть ли карта в каталоге или нет."""
        config_data = load_config_file()
        starmap_filename = config_data['starmap']['STARMAP_FILENAME']
        starmap_directory = os.path.join('media', 'clients', str(obj.id))
        if not os.path.exists(starmap_directory) or starmap_filename not in os.listdir(starmap_directory):
            return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False">')
        return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')

    def get_image(self, obj):
        """Отображение миниатюры полученной зездной карты."""
        config_data = load_config_file()
        starmap_filename = config_data['starmap']['STARMAP_FILENAME']
        starmap_directory = os.path.join('media', 'clients', str(obj.id))
        if not os.path.exists(starmap_directory) or starmap_filename not in os.listdir(starmap_directory):
            return 'Нет изображения'
        starmap_filepath = os.path.join("/media", "clients", str(obj.id), starmap_filename)
        return mark_safe(
            f'<a href="{starmap_filepath}" target="_blank">'
            f'<img src="{starmap_filepath}" width="100" height="100">'
            f'</a>')

    is_image.short_description = 'Карта загружена'
    get_image.short_description = 'Изображение'


# Настройка названия админки сайта
# TODO: каждая роль персонала отмечается цветом и настроить права доступа
admin.site.site_header = 'ASTROSTORI'
admin.site.site_title = 'ASTROSTORI'
