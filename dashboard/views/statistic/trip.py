from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from decimal import Decimal
from datetime import datetime
from django.utils import timezone
from order.models import Trip,Status,OrderConfig
from utils.decerators import staff_member_required
from django.contrib.auth.decorators import permission_required

@staff_member_required
def trips_per_month(request):
    current_year = timezone.now().year

    # Query to get trips count and total price_with_tax_with_coupon per month
    trip_data = Trip.objects.filter(createdAt__year=current_year) \
        .annotate(month=TruncMonth('createdAt')) \
        .values('month') \
        .annotate(trip_count=Count('id'), total_price_with_coupon=Sum('price')) \
        .order_by('month')

    # Format the data for chart.js
    months = []
    trip_counts = []
    total_prices = []

    for trip in trip_data:
        # Manually compute price_with_tax_with_coupon for each trip
        trips = Trip.objects.filter(createdAt__month=trip['month'].month)
        price_with_coupon_total = sum([t.price_with_tax_with_coupon() for t in trips])
        
        months.append(trip['month'].strftime("%B"))
        trip_counts.append(trip['trip_count'])
        total_prices.append(float(price_with_coupon_total))

    return JsonResponse({'months': months, 'trip_counts': trip_counts, 'total_prices': total_prices})

@permission_required("accounts.Statistics", raise_exception=True)
@staff_member_required
def get_trip_stats(request):
    # الحصول على معايير الفلترة من طلب GET
    filter_type = request.GET.get('filter_type')  # 'year', 'month', 'day'
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    trips = Trip.objects.all()

    if filter_type == 'year' and year:
        trips = trips.filter(tripDate__year=year)
        cancelled_trips_count=trips.filter(status=Status.CANCELLED).count()
        rejected_trip_count=trips.filter(status=Status.REJECTED).count()
        trips = trips.filter(status=Status.COMPLETED)
        trip_count = trips.count()
        trip_commission=trip_count*OrderConfig.objects.first().commission or 0
        trip_total_tax = sum([t.tax() for t in trips])
        trip_total_amount = sum([t.price_with_tax_with_coupon() for t in trips])
        trip_total_amount =f"{trip_total_amount:.2f}"
        return JsonResponse({
                                'filter': 'year',
                                'trip_count': trip_count,
                                'cancelled_trips_count':cancelled_trips_count,
                                'rejected_trip_count':rejected_trip_count,
                                'trip_commission':trip_commission,
                                'trip_total_tax':trip_total_tax,
                                'trip_total_amount': trip_total_amount,

                             })

    if filter_type == 'month' and year and month:
        trips = trips.filter(tripDate__year=year, tripDate__month=month)
       
        cancelled_trips_count=trips.filter(status=Status.CANCELLED).count()
        rejected_trip_count=trips.filter(status=Status.REJECTED).count()
        trips = trips.filter(status=Status.COMPLETED)
        trip_count = trips.count()
        trip_commission=trip_count*OrderConfig.objects.first().commission or 0
        trip_total_tax = sum([t.tax() for t in trips])
        trip_total_amount = sum([t.price_with_tax_with_coupon() for t in trips])
        trip_total_amount =f"{trip_total_amount:.2f}"
        return JsonResponse({
                                'filter': 'year',
                                'trip_count': trip_count,
                                'cancelled_trips_count':cancelled_trips_count,
                                'rejected_trip_count':rejected_trip_count,
                                'trip_commission':trip_commission,
                                'trip_total_tax':trip_total_tax,
                                'trip_total_amount': trip_total_amount,

                             })

    elif filter_type == 'day' and year and month and day:
        trips = trips.filter(tripDate__year=year, tripDate__month=month, tripDate__day=day,)
        cancelled_trips_count=trips.filter(status=Status.CANCELLED).count()
        rejected_trip_count=trips.filter(status=Status.REJECTED).count()
        trips = trips.filter(status=Status.COMPLETED)
        trip_count = trips.count()
        trip_commission=trip_count*OrderConfig.objects.first().commission or 0
        trip_total_tax = sum([t.tax() for t in trips])
        trip_total_amount = sum([t.price_with_tax_with_coupon() for t in trips])
        trip_total_amount =f"{trip_total_amount:.2f}"
        return JsonResponse({
                                'filter': 'year',
                                'trip_count': trip_count,
                                'cancelled_trips_count':cancelled_trips_count,
                                'rejected_trip_count':rejected_trip_count,
                                'trip_commission':trip_commission,
                                'trip_total_tax':trip_total_tax,
                                'trip_total_amount': trip_total_amount,

                             })

    else: 
        cancelled_trips_count=trips.filter(status=Status.CANCELLED).count()
        rejected_trip_count=trips.filter(status=Status.REJECTED).count()
        trips = trips.filter(status=Status.COMPLETED)
        trip_count = trips.count()
        trip_commission=trip_count*OrderConfig.objects.first().commission or 0
        trip_total_tax = sum([t.tax() for t in trips])
        trip_total_amount = sum([t.price_with_tax_with_coupon() for t in trips])
        trip_total_amount =f"{trip_total_amount:.2f}"
        return JsonResponse({
                                'filter': 'year',
                                'trip_count': trip_count,
                                'cancelled_trips_count':cancelled_trips_count,
                                'rejected_trip_count':rejected_trip_count,
                                'trip_commission':trip_commission,
                                'trip_total_tax':trip_total_tax,
                                'trip_total_amount': trip_total_amount,

                             })

        