from django.shortcuts import render, redirect,get_object_or_404
from ...forms.accounts.restaurant import RestaurantForm
from accounts.models import Restaurant,RestaurantSubscription
from django.db.models import Q
from wallet.models import UserWallet
from order.models import Order


def restaurant_financial_overview(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    wallet = get_object_or_404(UserWallet, user__id=restaurant_id)
    
    completed_order_number = Order.objects.filter(driver__isnull=False, status='COMPLETED', items__product__restaurant=restaurant).count()
    rejected_order_number = Order.objects.filter(driver__isnull=False, status='REJECTED', items__product__restaurant=restaurant).count()
    canceled_order_number = Order.objects.filter(driver__isnull=False, status='CANCELED', items__product__restaurant=restaurant).count()
    
    return render(request, 'accounts/restaurant/financial/overview.html', {
        'restaurant': restaurant,
        'wallet': wallet,
        'completed_order_number': completed_order_number,
        'rejected_order_number': rejected_order_number,
        'canceled_order_number':canceled_order_number,
    })
