from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from wallet.models import UserWallet
from accounts.models import Driver
from order.models import Order,Status
from datetime import datetime, date
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render
from order.models import Order,Trip
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def drivers_wallet_list(request):
    # Get all Driver instances
    drivers = Driver.objects.filter(enabled=True)

    # Get the UserWallet instances for the Driver users
    driver_wallets = UserWallet.objects.filter(user__in=drivers, balance__gt=0)
    return render(request,'financial/drivers/list.html',{'driver_wallets':driver_wallets})

def drivers_wallet_details(request,driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    wallet = get_object_or_404(UserWallet, user__id=driver_id)
     # Get the current date, month, and year
    current_date = date.today()
    current_month = timezone.now().month
    current_year = timezone.now().year
   
    # Retrieve orders for today
    today_orders = Order.objects.filter(
        driver=driver,
        status=Status.COMPLETED,
        orderDate__date=current_date
    )

    # Retrieve orders for this month
    month_orders = Order.objects.filter(
        driver=driver,
        status=Status.COMPLETED,
        orderDate__month=current_month
    )

    # Retrieve orders for this year
    year_orders = Order.objects.filter(
        driver=driver,
        status=Status.COMPLETED,
        orderDate__year=current_year
        )
    
    today_trips = Trip.objects.filter(
            driver=driver,
            status=Status.COMPLETED,
            createdAt__date=current_date
        )

    month_trips = Trip.objects.filter(
            driver=driver,
            status=Status.COMPLETED,
            createdAt__month=current_month
        )

    year_trips = Trip.objects.filter(
            driver=driver,
            status=Status.COMPLETED,
            createdAt__year=current_year
        )

    trip_today_price_sum = today_trips.aggregate(Sum('price'))['price__sum']
    trip_month_price_sum = month_trips.aggregate(Sum('price'))['price__sum']
    trip_year_price_sum = year_trips.aggregate(Sum('price'))['price__sum']

    # Calculate the sum of totalAmount for each time range
    today_total_amount_sum = today_orders.aggregate(Sum('deliveryCost'))['deliveryCost__sum']
    month_total_amount_sum = month_orders.aggregate(Sum('deliveryCost'))['deliveryCost__sum']
    year_total_amount_sum = year_orders.aggregate(Sum('deliveryCost'))['deliveryCost__sum']
    
    completed_order_number = Order.objects.filter(driver=driver, status='COMPLETED',).count()
    rejected_order_number = Order.objects.filter(driver=driver, status='REJECTED', ).count()
    canceled_order_number = Order.objects.filter(driver=driver, status='CANCELED',).count()
    
    completed_trips = Trip.objects.filter(driver=driver, status=Status.COMPLETED).count()

    cancelled_trips = Trip.objects.filter(driver=driver, status=Status.CANCELLED).count()

    rejected_trips = Trip.objects.filter(driver=driver, status=Status.REJECTED).count()

    wallet = get_object_or_404(UserWallet,user__id=driver_id)
    return render(request,'financial/drivers/details.html', {
        # 'driver': driver,
        'wallet': wallet,
        'completed_order_number': completed_order_number,
        'rejected_order_number': rejected_order_number,
        'canceled_order_number':canceled_order_number,
        'today_total_amount_sum':today_total_amount_sum,
        'month_total_amount_sum':month_total_amount_sum,
        'year_total_amount_sum':year_total_amount_sum,
        'completed_trips':completed_trips,
        'cancelled_trips':cancelled_trips,
        'rejected_trips':rejected_trips,
        'trip_today_price_sum':trip_today_price_sum,
        'trip_month_price_sum':trip_month_price_sum,
        'trip_year_price_sum':trip_year_price_sum
        
    })
    



from datetime import datetime

def driver_complated_orders(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    completad_orders = Order.objects.filter(driver=driver, status=Status.COMPLETED).order_by('-orderDate')

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
    
    return render(request, 'financial/drivers/orders.html', {'title': "الطلبات المكتملة",
                                                             'en_title': "Complated Oeders",
                                                             'url':'driver_complated_orders',
                                                             'orders': completad_orders,
                                                             'total_price':total_price,
                                                             'num_pages': num_pages,
                                                             'driver':driver
                                                             })

def driver_rejected_orders(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    rejected_orders = Order.objects.filter(driver=driver, status=Status.REJECTED).order_by('-orderDate')

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
    
    return render(request, 'financial/drivers/orders.html', {'title': "الطلبات الملغية",
                                                             'en_title': "Rejected Oeders",
                                                             'url':'driver_rejected_orders',
                                                             'orders': rejected_orders,
                                                             'total_price':total_price,
                                                             'num_pages': num_pages,
                                                             'driver':driver
                                                             })
    
def driver_cancelled_orders(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    cancelled_orders = Order.objects.filter(driver=driver, status=Status.REJECTED).order_by('-orderDate')

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
    
    return render(request, 'financial/drivers/orders.html', {'title': "الطلبات الملغية",
                                                             'en_title': "Cancelled Oeders",
                                                             'url':'driver_cancelled_orders',
                                                             'orders': cancelled_orders,
                                                             'total_price':total_price,
                                                             'num_pages': num_pages,
                                                             'driver':driver
                                                             })
    
    
def order_details(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'financial/drivers/order_details.html', {'order': order})



######TRIPS
def driver_complated_trips(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    completad_trips = Trip.objects.filter(driver=driver, status=Status.COMPLETED).order_by('-tripDate')

    # Date Filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        completad_trips = completad_trips.filter(tripDate__range=[start_date, end_date])
    total_price=0
    for trip in completad_trips:
        total_price+= trip.price_with_tax_with_coupon()
  
    # Pagination code remains the same

    num_pages = Paginator.num_pages  # Total number of pages
    
    return render(request, 'financial/drivers/trips.html', {'title': "الرحل  المكتملة",
                                                             'en_title': "Complated Trips",
                                                             'url':'driver_complated_trips',
                                                             'trips': completad_trips,
                                                             'total_price':total_price,
                                                             'num_pages': num_pages,
                                                             'driver':driver
                                                             })
    
def driver_rejected_trips(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    rejected_trips = Trip.objects.filter(driver=driver, status=Status.REJECTED).order_by('-tripDate')

    # Date Filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        rejected_trips = rejected_trips.filter(tripDate__range=[start_date, end_date])
    total_price=0
    for trip in rejected_trips:
        total_price+= trip.price_with_tax_with_coupon()
  
    # Pagination code remains the same

    num_pages = Paginator.num_pages  # Total number of pages
    
    return render(request, 'financial/drivers/trips.html', {'title': "الرحل  المرفوضة",
                                                             'en_title': "Rejected Trips",
                                                             'url':'driver_rejected_trips',
                                                             'trips': rejected_trips,
                                                             'total_price':total_price,
                                                             'num_pages': num_pages,
                                                             'driver':driver
                                                             })
    
       
def driver_cancelled_trips(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    cancelled_trips = Trip.objects.filter(driver=driver, status=Status.CANCELLED).order_by('-tripDate')

    # Date Filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        cancelled_trips = cancelled_trips.filter(tripDate__range=[start_date, end_date])
    total_price=0
    for trip in cancelled_trips:
        total_price+= trip.price_with_tax_with_coupon()
  
    # Pagination code remains the same

    num_pages = Paginator.num_pages  # Total number of pages
    
    return render(request, 'financial/drivers/trips.html', {'title': "الرحل  الملغية",
                                                             'en_title': "Cancelled Trips",
                                                             'url':'driver_cancelled_trips',
                                                             'trips': cancelled_trips,
                                                             'total_price':total_price,
                                                             'num_pages': num_pages,
                                                             'driver':driver
                                                             })
    
def trip_details(request, trip_id):
    trip = Trip.objects.get(pk=trip_id)
    return render(request, 'financial/drivers/trip_details.html', {'trip': trip})


