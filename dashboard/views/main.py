from django.shortcuts import render,redirect,HttpResponse
from accounts.models import *
from restaurant.models import Category
def main_dashboard(request):
    client_count=Client.objects.all().count()
    driver_count=Driver.objects.filter(enabled=True).count()
    restaurant_count=Restaurant.objects.filter(enabled=True).count()
    category_count=Category.objects.all().count()
    #Regesteration request count
    drivers_requests_counts = Driver.objects.filter(enabled=False).count()
    restaurant_requests_counts = Restaurant.objects.filter(enabled=False).count()
    regesteration_request_count=drivers_requests_counts+restaurant_requests_counts
    context={
        'client_count':client_count,
        'driver_count':driver_count,
        'restaurant_count':restaurant_count,
        'category_count':category_count,
        'regesteration_request_count':regesteration_request_count
    }
    return render(request,'main_dashboard.html',context=context)