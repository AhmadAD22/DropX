from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from accounts.models import User,Driver,Client,Restaurant,RestaurantSubscription,DriverOrderSubscription,DriverTripSubscription
from django.db.models.functions import TruncMonth
from wallet.models import RestaurantSubscriptionPayment,DriverOrderSubscriptionPayment,DriverTripSubscriptionPayment
from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models import Q

def user_statistics(request):
    # Get filter parameters from the request
    filter_type = request.GET.get('filter_type')  # 'year', 'month', 'day'
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    # Filter base query for users, clients, drivers, and restaurants
    client_filter = Q()
    driver_filter = Q()
    restaurant_filter = Q()
    restaurant_subscription_filter = Q()

    # if filter_type == 'year' and year:
    #     user_filter &= Q(created_at__year=year)
    #     client_filter &= Q(created_at__year=year)
    #     driver_filter &= Q(created_at__year=year)
    #     restaurant_filter &= Q(created_at__year=year)
    #     restaurant_subscription_filter &= Q(start_date__year=year)
    # if filter_type == 'month' and year and month:
    #     user_filter &= Q(created_at__year=year, created_at__month=month)
    #     client_filter &= Q(created_at__year=year, created_at__month=month)
    #     driver_filter &= Q(created_at__year=year, created_at__month=month)
    #     restaurant_filter &= Q(created_at__year=year, created_at__month=month)
    #     restaurant_subscription_filter &= Q(start_date__year=year, start_date__month=month)
    # elif filter_type == 'day' and year and month and day:
    #     user_filter &= Q(created_at__year=year, created_at__month=month, created_at__day=day)
    #     client_filter &= Q(created_at__year=year, created_at__month=month, created_at__day=day)
    #     driver_filter &= Q(created_at__year=year, created_at__month=month, created_at__day=day)
    #     restaurant_filter &= Q(created_at__year=year, created_at__month=month, created_at__day=day)
    #     restaurant_subscription_filter &= Q(start_date__year=year, start_date__month=month, start_date__day=day)

    # Apply filters and get counts
    client_count = Client.objects.filter(client_filter).count()
    driver_count = Driver.objects.filter(driver_filter).count()
    restaurant_count = Restaurant.objects.filter(restaurant_filter).count()
    
    # Count of paid and non-expired subscriptions
    current_time = timezone.now()
    restaurant_subscription_counts = RestaurantSubscription.objects.filter(restaurant_subscription_filter &
        Q(paid=True)& Q( end_date__gt=current_time)
    ).count()
    order_subscription_counts = DriverOrderSubscription.objects.filter(
            Q(paid=True)& Q( end_date__gt=current_time)
        ).count()
    
    trip_subscription_counts = DriverTripSubscription.objects.filter(
            Q(paid=True)& Q( end_date__gt=current_time)
        ).count()
    

    years = User.objects.dates('created_at', 'year').distinct()
    # Render results in template
    return render(request, 'statistics/user.html', {
        'client_count': client_count,
        'years': [year.year for year in years],
        'driver_count': driver_count,
        'restaurant_count': restaurant_count,
        'restaurant_subscription_counts': restaurant_subscription_counts,
        'order_subscription_counts':order_subscription_counts,
        'trip_subscription_counts':trip_subscription_counts
        
        
       
    })



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
