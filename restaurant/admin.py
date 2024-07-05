from django.contrib import admin
from .models import* 
admin.site.register(Product)
admin.site.register(AccessoryProduct)
admin.site.register(ProductReview)
admin.site.register(CommonQuestion)
admin.site.register(RestaurantOpening)
admin.site.register(RestaurantReview)

# Register your models here.
