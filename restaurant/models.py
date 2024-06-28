from django.db import models
from accounts.models import *
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.conf import settings
import os
from accounts.models import Restaurant

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/restaurant/category/',null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,blank=True,null=True)
    

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Delete the associated image file
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
                # Delete the file from the server
            if os.path.exists(image_path):
                os.remove(image_path)
        
        super(Category, self).delete(*args, **kwargs)

        
class Product(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,related_name='productRestaurant')
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name='productCategory')
    image = models.ImageField(upload_to='media/restaurant/products/',null=True,blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offers = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0,blank=False, verbose_name='الخصم')
    quantity = models.PositiveIntegerField()
    minimumOrder=models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء',blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث',blank=True,null=True)

    @property
    def price_after_offer(self):
        if self.offers is not None and self.price is not None:
            discount = Decimal(float(self.price)) * (Decimal(self.offers) / 100)
            return Decimal(self.price) - discount
        return self.price
    
    def delete(self, *args, **kwargs):
        # Delete the associated image file
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
                # Delete the file from the server
            if os.path.exists(image_path):
                os.remove(image_path)
        
        super(Product, self).delete(*args, **kwargs)
    def __str__(self) -> str:
        return self.name +'/'+self.restaurant.restaurantName
        

class AccessoryProduct(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField()
    
class RestaurantOpening(models.Model):
    DAY_CHOICES = [
    ("Sun", "الأحد"),
    ("Mon", "الاثنين"),
    ("Tue", "الثلاثاء"),
    ("Wed", "الأربعاء"),
    ("Thu", "الخميس"),
    ("Fri", "الجمعة"),
    ("Sat", "السبت"),
]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day = models.CharField(max_length=3,choices=DAY_CHOICES)
    time_start=models.TimeField()
    time_end=models.TimeField()
    Rest_time_start=models.TimeField(null=True,blank=True,auto_now=False, auto_now_add=False)
    Rest_time_end=models.TimeField(null=True,blank=True,auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_on =models.DateTimeField(auto_now=True,blank=True,null=True)
    
    def is_open(self):
        """
        Returns True if the restaurant is open at the current time, False otherwise.
        """
        now = datetime.now().time()
        if self.time_start <= now <= self.time_end:
            if self.Rest_time_start is None or self.Rest_time_end is None or self.Rest_time_start <= now <= self.Rest_time_end:
                return True
        return False


class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,null=True,blank=True,verbose_name='الزبون')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,verbose_name='المتجر')
    message = models.TextField(verbose_name='رسالة')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True, verbose_name='تقييم المنتج')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء',blank=True,null=True)

    
    def __str__(self):
        return f"Message by {self.client.username}"

class CommonQuestion(models.Model):
    restaurant=models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    question=models.CharField(max_length=255)
    answer=models.TextField()