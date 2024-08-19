from django.shortcuts import render, redirect,get_object_or_404
from ...forms.accounts.driver import DriverForm
from accounts.models import Driver,DriverOrderSubscription,DriverTripSubscription
from django.db.models import Q

def driver_list(request):
    search_query = request.GET.get('search', '')
    drivers = Driver.objects.filter(Q(enabled=True) &
        (Q(fullName__icontains=search_query) |
        Q(phone__icontains=search_query) |
        Q(email__icontains=search_query))
    )
    return render(request, 'accounts/driver/list.html', {'drivers': drivers, 'search_query': search_query})

def Driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            Driver = form.save()
            return redirect('Driver_list')
    else:
        form = DriverForm()
    return render(request, 'Driver_create.html', {'form': form})

def driver_details(request, pk):
    driver = get_object_or_404(Driver,pk=pk)
    return render(request, 'accounts/driver/details.html', {'driver':driver})



def driver_update(request, pk):
    driver = get_object_or_404(Driver,pk=pk)
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES, instance= driver)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm(instance= driver)
    return render(request, 'accounts/driver/update.html', {'form': form,'driver':driver})

def driver_delete(request, pk):
    driver = get_object_or_404(Driver,pk=pk)
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_list')
    
# Subscription   
def driver_subscription(request, pk):
    driver = get_object_or_404(Driver,pk=pk)
    order_subscriptions=DriverOrderSubscription.objects.filter(driver=driver)
    trip_subscriptions=DriverTripSubscription.objects.filter(driver=driver)
    return render(request, 'accounts/driver/subscription.html', {'driver':driver,'order_subscriptions':order_subscriptions,'trip_subscriptions':trip_subscriptions})
    
def driver_order_subscription_disable(request, pk):
    driver = get_object_or_404(Driver,pk=pk)
    order_subscriptions=DriverOrderSubscription.objects.filter(driver=driver)
    if order_subscriptions:
        for subscription in order_subscriptions:
            subscription.enabled=False
            subscription.save()
            print(subscription.enabled)
    return redirect('driver_subscription',pk)

def driver_order_subscription_enable(request, pk):
    driver = get_object_or_404(Driver,pk=pk)
    order_subscriptions=DriverOrderSubscription.objects.filter(driver=driver)
    if order_subscriptions:
        for subscription in order_subscriptions:
            subscription.enabled=True
            subscription.save()
            print(subscription.enabled)
    return redirect('driver_subscription',pk)

def driver_trip_subscription_desable(request, pk):
    driver = get_object_or_404(Driver,pk=pk)
    trip_subscriptions=DriverTripSubscription.objects.filter(driver=driver)
    if trip_subscriptions:
        for subscription in trip_subscriptions:
            subscription.enabled=False
            subscription.save()
    return redirect('driver_subscription',pk)

def driver_trip_subscription_enable(request, pk):
    driver = get_object_or_404(Driver,pk=pk)
    trip_subscriptions=DriverTripSubscription.objects.filter(driver=driver)
    if trip_subscriptions:
        for subscription in trip_subscriptions:
            subscription.enabled=True
            subscription.save()
    return redirect('driver_subscription',pk)