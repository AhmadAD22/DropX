from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from accounts.models import User,Driver
from django.db.models.functions import TruncMonth

from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncDay,TruncYear
from django.http import JsonResponse
from django.utils import timezone
from order.models import Order

def order_statistics(request):
    # الحصول على السنوات المتاحة للفلترة
    filter_type = request.GET.get('filter_type')  # 'year', 'month', 'day'
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    # تصفية الطلبات بناءً على الفلاتر المقدمة
    orders = Order.objects.all()

    if filter_type == 'year' and year:
        orders = orders.filter(orderDate__year=year)
    if filter_type == 'month' and year and month:
        orders = orders.filter(orderDate__year=year, orderDate__month=month)
    elif filter_type == 'day' and year and month and day:
        orders = orders.filter(orderDate__year=year, orderDate__month=month, orderDate__day=day)

    # حساب عدد الطلبات وإجمالي المبلغ
    order_count = orders.count()
    order_total_amount = orders.aggregate(total=Sum('totalAmount'))['total'] or 0

    years = Order.objects.dates('orderDate', 'year').distinct()
    
    context = {
        'request':request,
        'years': [year.year for year in years],
        'order_count':order_count,
        'order_total_amount':order_total_amount,
        
    }
    return render(request, 'statistic.html', context)


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
