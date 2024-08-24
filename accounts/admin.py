from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission
# Register your models here.
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Driver)
admin.site.register(Permission )
admin.site.register(Restaurant)
admin.site.register(PendingClient)
admin.site.register(OTPRequest)

admin.site.register(PendingDriver)
admin.site.register(Car)
admin.site.register(CarCategory)
admin.site.register(PendingRestaurant)
admin.site.register(RestaurantSubscription)
admin.site.register(Notification)
admin.site.register(SubscriptionConfig)
admin.site.register(DriverOrderSubscription)
admin.site.register(DriverTripSubscription)




