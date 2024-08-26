from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserWallet)
admin.site.register(PaymentOrder)
admin.site.register(PaymentTrip)
admin.site.register(RestaurantSubscriptionPayment)
admin.site.register(DriverOrderSubscriptionPayment)
admin.site.register(DriverTripSubscriptionPayment)