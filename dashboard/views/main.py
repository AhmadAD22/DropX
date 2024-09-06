from django.shortcuts import render,redirect,HttpResponse
from accounts.models import *
from restaurant.models import Category
from order.models import Trip,Order,OrderConfig,Status
from django.db.models import Sum
from wallet.models import DriverTripSubscriptionPayment,DriverOrderSubscriptionPayment,RestaurantSubscriptionPayment
def main_dashboard(request):
    client_count=Client.objects.all().count()
    driver_count=Driver.objects.filter(enabled=True).count()
    restaurant_count=Restaurant.objects.filter(enabled=True).count()
    category_count=Category.objects.all().count()
    #Regesteration request count
    drivers_requests_counts = Driver.objects.filter(enabled=False).count()
    restaurant_requests_counts = Restaurant.objects.filter(enabled=False).count()
    regesteration_request_count=drivers_requests_counts+restaurant_requests_counts
    #ORDER  PROFITS
    orders = Order.objects.filter(status=Status.COMPLETED)
    order_count = orders.count()
    order_commission=order_count*OrderConfig.objects.first().commission or 0
    trips = Trip.objects.filter(status=Status.COMPLETED)
    trip_count = trips.count()
    trip_commission=trip_count*OrderConfig.objects.first().commission or 0
    commission_profits=trip_commission+order_commission
    # SUBSCRIPTION PROFITS
    trip_subscriptios=DriverTripSubscriptionPayment.objects.filter(paid=True)
    trip_subscriptios_total_amount = trip_subscriptios.aggregate(total=Sum('price'))['total'] or 0
    order_subscriptios=DriverOrderSubscriptionPayment.objects.filter(paid=True)
    order_subscriptios_total_amount = order_subscriptios.aggregate(total=Sum('price'))['total'] or 0
    restaurant_subscription=RestaurantSubscriptionPayment.objects.filter(paid=True)
    restaurant_subscription_total_amount = restaurant_subscription.aggregate(total=Sum('price'))['total'] or 0
    subscription_profits=restaurant_subscription_total_amount+trip_subscriptios_total_amount+order_subscriptios_total_amount
    context={
        'client_count':client_count,
        'driver_count':driver_count,
        'restaurant_count':restaurant_count,
        'category_count':category_count,
        'regesteration_request_count':regesteration_request_count,
        'commission_profits':commission_profits,
        'subscription_profits':subscription_profits
    }
    return render(request,'main_dashboard.html',context=context)