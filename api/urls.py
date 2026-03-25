from django.urls import path
from .views import getListOfHotels, reservationConfirmation

urlpatterns = [
    path('hotels/', getListOfHotels, name='get_hotels'),
    path('reservations/confirm/', reservationConfirmation, name='reservation_confirmation'),
]