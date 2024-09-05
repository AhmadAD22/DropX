from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from wallet.models import UserWallet
from accounts.models import Restaurant
from order.models import Order,Status
from datetime import datetime, date
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render
from order.models import Order,Trip
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def restaurants_wallet_list(request):
    # Get all restaurant instances
    restaurants = Restaurant.objects.filter(enabled=True)
    # Get the UserWallet instances for the restaurant users
    restaurant_wallets = UserWallet.objects.filter(user__in=restaurants, balance__gt=0)
    print(restaurant_wallets.count())
    return render(request,'financial/restaurant/list.html',{'restaurant_wallets':restaurant_wallets})

def restaurants_wallet_details(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    wallet = get_object_or_404(UserWallet, user__id=restaurant_id)
     # Get the current date, month, and year
    current_date = date.today()
    current_month = timezone.now().month
    current_year = timezone.now().year
   
    # Retrieve orders for today
    today_orders = Order.objects.filter(
        items__product__restaurant=restaurant,
        status=Status.COMPLETED,
        orderDate__date=current_date
    )

    # Retrieve orders for this month
    month_orders = Order.objects.filter(
        items__product__restaurant=restaurant,
        status=Status.COMPLETED,
        orderDate__month=current_month
    )

    # Retrieve orders for this year
    year_orders = Order.objects.filter(
        items__product__restaurant=restaurant,
        status=Status.COMPLETED,
        orderDate__year=current_year
        )
   
    # Calculate the sum of totalAmount for each time range
    today_total_amount_sum = today_orders.aggregate(Sum('totalAmount'))['totalAmount__sum']
    month_total_amount_sum = month_orders.aggregate(Sum('totalAmount'))['totalAmount__sum']
    year_total_amount_sum = year_orders.aggregate(Sum('totalAmount'))['totalAmount__sum']

    
    completed_order_number = Order.objects.filter(items__product__restaurant=restaurant, status='COMPLETED',).count()
    rejected_order_number = Order.objects.filter(items__product__restaurant=restaurant, status='REJECTED', ).count()
    canceled_order_number = Order.objects.filter(items__product__restaurant=restaurant, status='CANCELED',).count()
    
    wallet = get_object_or_404(UserWallet,user__id=restaurant_id)
    return render(request,'financial/restaurant/details.html', {
        # 'restaurant': restaurant,
        'wallet': wallet,
        'completed_order_number': completed_order_number,
        'rejected_order_number': rejected_order_number,
        'canceled_order_number':canceled_order_number,
        'today_total_amount_sum':today_total_amount_sum,
        'month_total_amount_sum':month_total_amount_sum,
        'year_total_amount_sum':year_total_amount_sum,
    
        
    })