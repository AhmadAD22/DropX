from openpyxl import Workbook
from django.http import HttpResponse
from accounts.models import Driver ,Restaurant
from wallet.models import UserWallet,PaymentTrip,PaymentOrder
from django.db.models import Sum
from django.utils import timezone
from utils.decerators import staff_member_required
from django.contrib.auth.decorators import permission_required



@permission_required("accounts.Financial", raise_exception=True)
@staff_member_required
def driver_generate_excel(request):
    drivers = Driver.objects.filter(enabled=True)
    # Get the UserWallet instances for the Driver users
    driver_wallets = UserWallet.objects.filter(user__in=drivers, balance__gt=0)
    if driver_wallets:
        # Create a new Excel 
        wb = Workbook()
        ws = wb.active
        
        # Add data to the Excel sheet
        
        ws.append(['الإسم', 'رقم الهاتف','اسم البنك','أيبان','عدد طلبات  نقل الأفراد','عدد طلبات المطعم','اجمالي قيمة الفواتير','المبلغ المستحق'])
        for driver_wallet in driver_wallets:
            trips=PaymentTrip.objects.all()
            orders=PaymentOrder.objects.all()
            if driver_wallet.last_withdrawal is None:
                trips=trips.filter(trip__driver=driver_wallet.user.driver,confirmed=True)
                orders=orders.filter(order__driver=driver_wallet.user.driver,confirmed=True)
            else:
                trips=trips.filter(trip__driver=driver_wallet.user.driver,confirmed=True,date__gt=driver_wallet.last_withdrawal)
                orders=orders.filter(order__driver=driver_wallet.user.driver,confirmed=True,date__gt=driver_wallet.last_withdrawal)
            orders_counts=orders.count()
            order_total_price=orders.aggregate(total_price=Sum('amount'))['total_price'] or 0
            trip_counts=trips.count()
            trip_total_price=trips.aggregate(total_price=Sum('amount'))['total_price'] or 0
            total_price=trip_total_price+order_total_price
            
            ws.append([driver_wallet.user.fullName, driver_wallet.user.phone,driver_wallet.user.driver.bankName,driver_wallet.user.driver.iban,trip_counts,orders_counts,total_price,driver_wallet.balance])
            driver_wallet.balance=0.0
            driver_wallet.last_withdrawal=timezone.now()
            driver_wallet.save()
        # Save the workbook
        current_date = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')  # Format date and time
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Drivers_{current_date}.xlsx"'
        wb.save(response)

        return response
    else:
        return HttpResponse('خطأ لا يوجد مستحاق لدفعها')
    
@permission_required("accounts.Financial", raise_exception=True)
@staff_member_required
def restaurant_generate_excel(request):
    restaurants = Restaurant.objects.filter(enabled=True)
    # Get the UserWallet instances for the Driver users
    restaurant_wallets = UserWallet.objects.filter(user__in=restaurants, balance__gt=0)
    if restaurant_wallets:
        # Create a new Excel 
        wb = Workbook()
        ws = wb.active
        
        # Add data to the Excel sheet
        
        ws.append(['الإسم', 'رقم الهاتف','اسم البنك','أيبان','عدد طلبات المطعم','اجمالي قيمة الفواتير','المبلغ المستحق'])
        for restaurant_wallet in restaurant_wallets:
            orders=PaymentOrder.objects.all()
            if restaurant_wallets.last_withdrawal is None:
                orders=orders.filter(order__items__product__restaurant=restaurant_wallet.user.restaurant,confirmed=True).distinct()
            else:
                orders=orders.filter(order__items__product__restaurant=restaurant_wallet.user.restaurant,confirmed=True,date__gt=restaurant_wallet.last_withdrawal).distinct()
            orders_counts=orders.count()
            order_total_price=orders.aggregate(total_price=Sum('amount'))['total_price'] or 0            
            ws.append([restaurant_wallet.user.fullName, restaurant_wallet.user.phone,restaurant_wallet.user.restaurant.bankName,restaurant_wallet.user.restaurant.iban,orders_counts,order_total_price,restaurant_wallet.balance])
            restaurant_wallet.balance=0.0
            restaurant_wallet.last_withdrawal=timezone.now()
            restaurant_wallet.save()
        # Save the workbook
        current_date = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')  # Format date and time
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Restaurants_{current_date}.xlsx"'
        wb.save(response)

        return response
    else:
        return HttpResponse('خطأ لا يوجد مستحاق لدفعها')