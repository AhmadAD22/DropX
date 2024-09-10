from django.shortcuts import render, redirect,get_object_or_404
from accounts.models import Driver,DriverTripSubscription
from wallet.models import UserWallet
from order.models import Order
from utils.decerators import staff_member_required
from django.contrib.auth.decorators import permission_required



@permission_required("accounts.Driver", raise_exception=True)
@staff_member_required
def driver_financial_overview(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    wallet = get_object_or_404(UserWallet, user__id=driver_id)
    
    completed_order_number = Order.objects.filter(driver=driver, status='COMPLETED',).count()
    rejected_order_number = Order.objects.filter(driver=driver, status='REJECTED', ).count()
    canceled_order_number = Order.objects.filter(driver=driver, status='CANCELED',).count()
    
    return render(request, 'accounts/driver/financial/overview.html', {
        'driver': driver,
        'wallet': wallet,
        'completed_order_number': completed_order_number,
        'rejected_order_number': rejected_order_number,
        'canceled_order_number':canceled_order_number,
    })
