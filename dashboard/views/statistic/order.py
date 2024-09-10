from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from order.models import Order,Status,OrderConfig
from utils.decerators import staff_member_required
from utils.decerators import staff_member_required
from django.contrib.auth.decorators import permission_required

@permission_required("accounts.Statistics", raise_exception=True)
@staff_member_required
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


@staff_member_required
def orders_per_month(request):
    current_year = timezone.now().year
    
    # Query to get orders count and total price per month
    order_data = Order.objects.filter(orderDate__year=current_year) \
        .annotate(month=TruncMonth('orderDate')) \
        .values('month') \
        .annotate(order_count=Count('id'), total_price=Sum('totalAmount')) \
        .order_by('month')

    # Format the data for chart.js
    months = []
    order_counts = []
    total_prices = []
    
    for data in order_data:
        months.append(data['month'].strftime("%B"))
        order_counts.append(data['order_count'])
        total_prices.append(float(data['total_price']) if data['total_price'] else 0)

    return JsonResponse({'months': months, 'order_counts': order_counts, 'total_prices': total_prices})



# views.py

from django.shortcuts import render
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncDay
from django.http import JsonResponse
from django.utils import timezone

@permission_required("accounts.Statistics", raise_exception=True)
@staff_member_required
def get_order_stats(request):
    # الحصول على معايير الفلترة من طلب GET
    filter_type = request.GET.get('filter_type')  # 'year', 'month', 'day'
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    orders = Order.objects.all()

    if filter_type == 'year' and year:
        orders=orders = orders.filter(orderDate__year=year)
        cenceled_order_count=orders.filter(status=Status.CANCELLED).count()
        rejected_order_count=orders.filter(status=Status.REJECTED).count()
        orders = orders.filter(status=Status.COMPLETED)
        order_count = orders.count()
        order_commission=order_count*OrderConfig.objects.first().commission or 0
        order_total_tax = sum([o.tax() for o in orders])
        order_total_amount = orders.aggregate(total=Sum('totalAmount'))['total'] or 0
        order_total_amount =f"{order_total_amount:.2f}"
        
        return JsonResponse({'filter': 'year',
                             'cenceled_order_count':cenceled_order_count,
                             'rejected_order_count':rejected_order_count,
                             'order_count': order_count,
                             'order_commission':order_commission,
                             'order_total_tax':order_total_tax,
                             'order_total_amount': order_total_amount})

    if filter_type == 'month' and year and month:
        orders=orders = orders.filter(orderDate__year=year, orderDate__month=month)
        cenceled_order_count=orders.filter(status=Status.CANCELLED).count()
        rejected_order_count=orders.filter(status=Status.REJECTED).count()
        orders = orders.filter(status=Status.COMPLETED)
        order_count = orders.count()
        order_commission=order_count*OrderConfig.objects.first().commission or 0
        order_total_tax = sum([o.tax() for o in orders])
        order_total_amount = orders.aggregate(total=Sum('totalAmount'))['total'] or 0
        order_total_amount =f"{order_total_amount:.2f}"
        
        return JsonResponse({'filter': 'month',
                             'cenceled_order_count':cenceled_order_count,
                             'rejected_order_count':rejected_order_count,
                             'order_count': order_count,
                             'order_commission':order_commission,
                             'order_total_tax':order_total_tax,
                             'order_total_amount': order_total_amount})
        
    elif filter_type == 'day' and year and month and day:
        orders=orders = orders.filter(orderDate__year=year, orderDate__month=month, orderDate__day=day,)
        cenceled_order_count=orders.filter(status=Status.CANCELLED).count()
        rejected_order_count=orders.filter(status=Status.REJECTED).count()
        orders = orders.filter(status=Status.COMPLETED)
        order_count = orders.count()
        order_commission=order_count*OrderConfig.objects.first().commission or 0
        order_total_tax = sum([o.tax() for o in orders])
        order_total_amount = orders.aggregate(total=Sum('totalAmount'))['total'] or 0
        order_total_amount =f"{order_total_amount:.2f}"
        
        return JsonResponse({'filter': 'day',
                             'cenceled_order_count':cenceled_order_count,
                             'rejected_order_count':rejected_order_count,
                             'order_count': order_count,
                             'order_commission':order_commission,
                             'order_total_tax':order_total_tax,
                             'order_total_amount': order_total_amount})
    else: 
        cenceled_order_count=orders.filter(status=Status.CANCELLED).count()
        rejected_order_count=orders.filter(status=Status.REJECTED).count()
        orders=orders.filter(status=Status.COMPLETED)
        order_count = orders.count()
        order_commission=order_count*OrderConfig.objects.first().commission or 0
        order_total_tax = sum([o.tax() for o in orders])
        order_total_amount = orders.aggregate(total=Sum('totalAmount'))['total'] or 0
        order_total_amount =f"{order_total_amount:.2f}"
        
        return JsonResponse({'filter': 'all',
                             'cenceled_order_count':cenceled_order_count,
                             'rejected_order_count':rejected_order_count,
                             'order_count': order_count,
                             'order_commission':order_commission,
                             'order_total_tax':order_total_tax,
                             'order_total_amount': order_total_amount})
    # حساب عدد الطلبات وإجمالي المبلغ
   
    # orders = Order.objects.all()
    # if filter_type == 'year' and year:
    #     orders = orders.filter(orderDate__year=year)
    #     months = [data['month'].strftime("%B") for data in order_data]
    #     order_counts = [data['order_count'] for data in order_data]
    #     total_amounts = [float(data['total_amount']) if data['total_amount'] else 0 for data in order_data]

    #     return JsonResponse({'filter': 'year', 'labels': months, 'order_counts': order_counts, 'total_amounts': total_amounts})

    # elif filter_type == 'month' and year and month:
    #     orders = orders.filter(orderDate__year=year, orderDate__month=month)
    #     # تجميع البيانات حسب اليوم
    #     order_data = orders.annotate(day=TruncDay('orderDate')).values('day') \
    #         .annotate(order_count=Count('id'), total_amount=Sum('totalAmount')) \
    #         .order_by('day')

    #     days = [data['day'].strftime("%d") for data in order_data]
    #     order_counts = [data['order_count'] for data in order_data]
    #     total_amounts = [float(data['total_amount']) if data['total_amount'] else 0 for data in order_data]

    #     return JsonResponse({'filter': 'month', 'labels': days, 'order_counts': order_counts, 'total_amounts': total_amounts})

    # elif filter_type == 'day' and year and month and day:
    #     orders = orders.filter(orderDate__year=year, orderDate__month=month, orderDate__day=day)
    #     total_orders = orders.count()
    #     total_amount = orders.aggregate(total=Sum('totalAmount'))['total'] or 0

    #     return JsonResponse({'filter': 'day', 'total_orders': total_orders, 'total_amount': float(total_amount)})

    # else:
    #     # إفتراضي: تجميع حسب الشهر للسنة الحالية
    #     current_year = timezone.now().year
    #     orders = orders.filter(orderDate__year=current_year)
    #     order_data = orders.annotate(month=TruncMonth('orderDate')).values('month') \
    #         .annotate(order_count=Count('id'), total_amount=Sum('totalAmount')) \
    #         .order_by('month')

    #     months = [data['month'].strftime("%B") for data in order_data]
    #     order_counts = [data['order_count'] for data in order_data]
    #     total_amounts = [float(data['total_amount']) if data['total_amount'] else 0 for data in order_data]

    #     return JsonResponse({'filter': 'year', 'labels': months, 'order_counts': order_counts, 'total_amounts': total_amounts})
