from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Hotel, Reservation
from .serializers import HotelSerializer, ReservationSerializer


@api_view(['GET'])
def getListOfHotels(request):
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    if not checkin or not checkout:
        return Response(
            {'error': 'checkin and checkout query parameters are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # find hotels that already have overlapping reservations
    unavailable_hotel_ids = Reservation.objects.filter(
        checkin__lt=checkout,
        checkout__gt=checkin
    ).values_list('hotel_id', flat=True)

    # available hotels = all hotels except unavailable ones
    available_hotels = Hotel.objects.exclude(id__in=unavailable_hotel_ids)

    serializer = HotelSerializer(available_hotels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def reservationConfirmation(request):
    serializer = ReservationSerializer(data=request.data)

    if serializer.is_valid():
        reservation = serializer.save()
        return Response(
            {'confirmation_number': reservation.confirmation_number},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)