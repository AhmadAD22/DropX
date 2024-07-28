from django.shortcuts import render,redirect,HttpResponse
from accounts.models import *
from restaurant.models import Category
def main_dashboard(request):
    client_count=Client.objects.all().count()
    driver_count=Driver.objects.all().count()
    restaurant_count=Restaurant.objects.all().count()
    category_count=Category.objects.all().count()
    context={
        'client_count':client_count,
        'driver_count':driver_count,
        'restaurant_count':restaurant_count,
        'category_count':category_count
    }
    return render(request,'main_dashboard.html',context=context)