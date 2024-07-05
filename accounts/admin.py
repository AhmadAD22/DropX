from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Client)
admin.site.register(Driver)
admin.site.register(Restaurant)

admin.site.register(PendingClient)
admin.site.register(OTPRequest)
admin.site.register(MembersServiceSubscription)
admin.site.register(OrderServiceSubscription)
admin.site.register(PendingDriver)
admin.site.register(Car)

admin.site.register(PendingRestaurant)
admin.site.register(RestaurantSubscription)
admin.site.register(Notification)





