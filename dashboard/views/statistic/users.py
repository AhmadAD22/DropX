from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from accounts.models import User,Driver,Client,Restaurant,RestaurantSubscription,DriverOrderSubscription,DriverTripSubscription
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models import Q
from utils.decerators import staff_member_required
from django.contrib.auth.decorators import permission_required

@permission_required("accounts.Statistics", raise_exception=True)
@staff_member_required
def user_statistics(request):
    years = User.objects.dates('created_at', 'year').distinct()
    # Render results in template
    return render(request, 'statistics/user.html', {
        'years': [year.year for year in years],
    })

@permission_required("accounts.Statistics", raise_exception=True)
@staff_member_required
def get_user_stats(request):
    # Get filter parameters from the request
    filter_type = request.GET.get('filter_type')  # 'year', 'month', 'day'
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    # Base query for filtering clients, drivers, restaurants, and subscriptions
    clients = Client.objects.all()
    drivers = Driver.objects.all()
    restaurants = Restaurant.objects.all()
    restaurant_subscriptions = RestaurantSubscription.objects.filter(paid=True, end_date__gt=timezone.now())
    order_subscriptions = DriverOrderSubscription.objects.filter(paid=True, end_date__gt=timezone.now())
    trip_subscriptions = DriverTripSubscription.objects.filter(paid=True, end_date__gt=timezone.now())
    # Filtering by year
    if filter_type == 'year' and year:
        clients = clients.filter(created_at__year=year)
        drivers = drivers.filter(created_at__year=year)
        restaurants = restaurants.filter(created_at__year=year)
        restaurant_subscriptions = restaurant_subscriptions.filter(start_date__year=year)
        trip_subscriptions=trip_subscriptions.filter(start_date__year=year)
        order_subscriptions=order_subscriptions.filter(start_date__year=year)
        # Count statistics
        client_count = clients.count()
        driver_count = drivers.count()
        restaurant_count = restaurants.count()
        order_subscriptions_count=order_subscriptions.count()
        trip_subscriptions_count=trip_subscriptions.count()
        restaurant_subscription_count = restaurant_subscriptions.count()

        return JsonResponse({
            'filter': 'year',
            'client_count': client_count,
            'driver_count': driver_count,
            'restaurant_count': restaurant_count,
            'restaurant_subscription_count': restaurant_subscription_count,
            'order_subscriptions_count':order_subscriptions_count,
            'trip_subscriptions_count':trip_subscriptions_count
        })

    # Filtering by month
    elif filter_type == 'month' and year and month:
        clients = clients.filter(created_at__year=year, created_at__month=month)
        drivers = drivers.filter(created_at__year=year, created_at__month=month)
        restaurants = restaurants.filter(created_at__year=year, created_at__month=month)
        restaurant_subscriptions = restaurant_subscriptions.filter(start_date__year=year, start_date__month=month)

        trip_subscriptions=trip_subscriptions.filter(start_date__year=year, start_date__month=month)
        order_subscriptions=order_subscriptions.filter(start_date__year=year, start_date__month=month)
        # Count statistics
        client_count = clients.count()
        driver_count = drivers.count()
        restaurant_count = restaurants.count()
        order_subscriptions_count=order_subscriptions.count()
        trip_subscriptions_count=trip_subscriptions.count()
        restaurant_subscription_count = restaurant_subscriptions.count()

        return JsonResponse({
            'filter': 'month',
            'client_count': client_count,
            'driver_count': driver_count,
            'restaurant_count': restaurant_count,
            'restaurant_subscription_count': restaurant_subscription_count,
            'order_subscriptions_count':order_subscriptions_count,
            'trip_subscriptions_count':trip_subscriptions_count
        })

    # Filtering by day
    elif filter_type == 'day' and year and month and day:
        clients = clients.filter(created_at__year=year, created_at__month=month, created_at__day=day)
        drivers = drivers.filter(created_at__year=year, created_at__month=month, created_at__day=day)
        restaurants = restaurants.filter(created_at__year=year, created_at__month=month, created_at__day=day)
        restaurant_subscriptions = restaurant_subscriptions.filter(start_date__year=year, start_date__month=month, start_date__day=day)

        trip_subscriptions=trip_subscriptions.filter(start_date__year=year, start_date__month=month, start_date__day=day)
        order_subscriptions=order_subscriptions.filter(start_date__year=year, start_date__month=month, start_date__day=day)
        # Count statistics
        client_count = clients.count()
        driver_count = drivers.count()
        restaurant_count = restaurants.count()
        order_subscriptions_count=order_subscriptions.count()
        trip_subscriptions_count=trip_subscriptions.count()
        restaurant_subscription_count = restaurant_subscriptions.count()

        return JsonResponse({
            'filter': 'day',
            'client_count': client_count,
            'driver_count': driver_count,
            'restaurant_count': restaurant_count,
            'restaurant_subscription_count': restaurant_subscription_count,
            'order_subscriptions_count':order_subscriptions_count,
            'trip_subscriptions_count':trip_subscriptions_count
        })
    else:
        client_count = clients.count()
        driver_count = drivers.count()
        restaurant_count = restaurants.count()
        order_subscriptions_count=order_subscriptions.count()
        trip_subscriptions_count=trip_subscriptions.count()
        restaurant_subscription_count = restaurant_subscriptions.count()

        return JsonResponse({
            'filter': 'day',
            'client_count': client_count,
            'driver_count': driver_count,
            'restaurant_count': restaurant_count,
            'restaurant_subscription_count': restaurant_subscription_count,
            'order_subscriptions_count':order_subscriptions_count,
            'trip_subscriptions_count':trip_subscriptions_count
        })

@staff_member_required
def users_per_month(request):
    current_year = timezone.now().year
    user_data = Driver.objects.filter(created_at__year=current_year) \
        .annotate(month=TruncMonth('created_at')) \
        .values('month') \
        .annotate(user_count=Count('id')) \
        .order_by('month')

    # Format the data for chart.js
    months = []
    counts = []
    for data in user_data:
        months.append(data['month'].strftime("%B"))
        counts.append(data['user_count'])

    return JsonResponse({'months': months, 'counts': counts})
