from django.urls import path

from .views import form, get_starmap_order


urlpatterns = [
    path('', form, name='order'),
    path('get-starmap-order/', get_starmap_order, name='get_starmap_order'),
]
