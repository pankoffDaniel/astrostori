from django.urls import path

from .views import form, get_order


urlpatterns = [
    path('', form, name='order'),
    path('get-order/', get_order, name='get_order'),
]
