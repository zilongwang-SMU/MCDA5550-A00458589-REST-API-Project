

# Register your models here.
from django.contrib import admin
from .models import Hotel, Reservation, Guest

admin.site.register(Hotel)
admin.site.register(Reservation)
admin.site.register(Guest)