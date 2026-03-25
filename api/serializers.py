from rest_framework import serializers
from .models import Hotel, Reservation, Guest


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'hotel_name', 'city', 'total_rooms']


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['guest_name', 'gender']


class ReservationSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(write_only=True)
    guests_list = GuestSerializer(many=True, write_only=True)
    confirmation_number = serializers.CharField(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'hotel_name',
            'checkin',
            'checkout',
            'guests_list',
            'confirmation_number',
        ]

    def validate(self, data):
        hotel_name = data.get('hotel_name')
        checkin = data.get('checkin')
        checkout = data.get('checkout')
        guests_list = data.get('guests_list')

        # check hotel exists
        try:
            hotel = Hotel.objects.get(hotel_name=hotel_name)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({
                'hotel_name': 'Hotel does not exist.'
            })

        # check dates
        if checkin >= checkout:
            raise serializers.ValidationError({
                'date': 'Checkout date must be later than checkin date.'
            })

        # check guest list
        if not guests_list or len(guests_list) == 0:
            raise serializers.ValidationError({
                'guests_list': 'At least one guest is required.'
            })

        # check hotel availability (date overlap)
        overlapping_reservations = Reservation.objects.filter(
            hotel=hotel,
            checkin__lt=checkout,
            checkout__gt=checkin
        )

        if overlapping_reservations.exists():
            raise serializers.ValidationError({
                'hotel': 'This hotel is not available for the selected dates.'
            })

        data['hotel'] = hotel
        return data

    def create(self, validated_data):
        hotel = validated_data.pop('hotel')
        validated_data.pop('hotel_name')
        guests_list = validated_data.pop('guests_list')

        reservation = Reservation.objects.create(hotel=hotel, **validated_data)

        for guest_data in guests_list:
            Guest.objects.create(reservation=reservation, **guest_data)

        return reservation