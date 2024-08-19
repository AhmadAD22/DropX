from django.shortcuts import render, redirect,get_object_or_404
from order.models import Coupon
from ..forms.coupon import CouponForm
from django.db.models import Q
from accounts.models import Restaurant,Driver

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def coupon_list(request):
    search_query = request.GET.get('search', '')
    print(search_query)
    coupons = Coupon.objects.filter(code__icontains=search_query)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(coupons, 5)  # Show 10 coupons per page
    try:
        coupons = paginator.page(page)
    except PageNotAnInteger:
        coupons = paginator.page(1)
    except EmptyPage:
        coupons = paginator.page(paginator.num_pages)
    
    num_pages = paginator.num_pages  # Total number of pages
    
    return render(request, 'coupon/list.html', {'coupons': coupons, 'num_pages': num_pages})

def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponForm()
        
    form.fields['restaurant'].queryset = Restaurant.objects.all()
    form.fields['driver'].queryset = Driver.objects.all()
    return render(request, 'coupon/add.html', {'form': form})

def update_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('coupon_list')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'coupon/update.html', {'form': form,'coupon':coupon})

def delete_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        return redirect('coupon_list')