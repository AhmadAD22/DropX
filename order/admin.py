from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderAccessory)
admin.site.register(Coupon)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CartAccessory)
admin.site.register(TripCar)
admin.site.register(Trip)
admin.site.register(OrderConfig)






