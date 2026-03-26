from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Hotel, Reservation
from .serializers import HotelSerializer, ReservationSerializer


@api_view(['GET'])
def home(request):
    return Response(
        {
            'message': 'Hotel Reservation API is running.',
            'endpoints': {
                'home': '/',
                'admin': '/admin/',
                'get_hotels': '/api/hotels/?checkin=YYYY-MM-DD&checkout=YYYY-MM-DD',
                'reservation_confirmation': '/api/reservations/confirm/',
            }
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def getListOfHotels(request):
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    if not checkin or not checkout:
        return Response(
            {'error': 'checkin and checkout query parameters are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()
    except ValueError:
        return Response(
            {'error': 'Date format must be YYYY-MM-DD.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if checkin_date >= checkout_date:
        return Response(
            {'error': 'Checkout date must be later than checkin date.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    unavailable_hotel_ids = Reservation.objects.filter(
        checkin__lt=checkout_date,
        checkout__gt=checkin_date
    ).values_list('hotel_id', flat=True)

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