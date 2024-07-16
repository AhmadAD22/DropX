from django.db import models
from accounts.models import Client,Driver
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class DriverReview(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,null=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE,related_name='driverreview')
    message = models.TextField(verbose_name='رسالة')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)