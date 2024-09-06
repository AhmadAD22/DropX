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

    
    completed_order_number = Order.objects.filter(items__product__restaurant=restaurant, status=Status.COMPLETED,).distinct().count()
    rejected_order_number = Order.objects.filter(items__product__restaurant=restaurant, status=Status.REJECTED, ).distinct().count()
    canceled_order_number = Order.objects.filter(items__product__restaurant=restaurant, status=Status.CANCELLED,).distinct().count()
    
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
    
    

def restaurant_complated_orders(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    completad_orders = Order.objects.filter(items__product__restaurant=restaurant, status=Status.COMPLETED).distinct().order_by('-orderDate')

    # Date Filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        completad_orders = completad_orders.filter(orderDate__range=[start_date, end_date])
    total_price=0
    for order in completad_orders:
        total_price+= order.price_with_tax_with_coupon()
  
    # Pagination code remains the same

    num_pages = Paginator.num_pages  # Total number of pages
    
    return render(request, 'financial/restaurant/orders.html', {'title': "الطلبات المكتملة",
                                                             'en_title': "Complated Oeders",
                                                             'url':'restaurant_complated_orders',
                                                             'orders': completad_orders,
                                                             'total_price':total_price,
                                                             'num_pages': num_pages,
                                                             'restaurant':restaurant
                                                             })
def rsetaurant_order_details(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'financial/restaurant/order_details.html', {'order': order})

def restaurant_rejected_orders(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    rejected_orders = Order.objects.filter(items__product__restaurant=restaurant, status=Status.REJECTED).distinct().order_by('-orderDate')

    # Date Filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        rejected_orders = rejected_orders.filter(orderDate__range=[start_date, end_date])
    total_price=0
    for order in rejected_orders:
        total_price+= order.price_with_tax_with_coupon()
  
    # Pagination code remains the same

    num_pages = Paginator.num_pages  # Total number of pages
    
    return render(request, 'financial/restaurant/orders.html', {'title': "الطلبات الملغية",
                                                             'en_title': "Rejected Oeders",
                                                             'url':'restaurant_rejected_orders',
                                                             'orders': rejected_orders,
                                                             'total_price':total_price,
                                                             'num_pages': num_pages,
                                                             'restaurant':restaurant
                                                             })
    
def restaurant_cancelled_orders(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    cancelled_orders = Order.objects.filter(items__product__restaurant=restaurant, status=Status.CANCELLED).distinct().order_by('-orderDate')

    # Date Filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        cancelled_orders = cancelled_orders.filter(orderDate__range=[start_date, end_date])
    total_price=0
    for order in cancelled_orders:
        total_price+= order.price_with_tax_with_coupon()
  
    # Pagination code remains the same

    num_pages = Paginator.num_pages  # Total number of pages
    
    return render(request, 'financial/restaurant/orders.html', {'title': "الطلبات الملغية",
                                                             'en_title': "Cancelled Oeders",
                                                             'url':'restaurant_cancelled_orders',
                                                             'orders': cancelled_orders,
                                                             'total_price':total_price,
                                                             'num_pages': num_pages,
                                                             'restaurant':restaurant
                                                             })