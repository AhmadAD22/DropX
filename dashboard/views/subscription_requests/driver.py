from django.shortcuts import render, redirect,get_object_or_404
from ...forms.accounts.driver import DriverForm
from accounts.models import Driver
from django.db.models import Q
from utils.notifications import NotificationsHelper,RegistrationUpdate
from utils.decerators import staff_member_required
from django.contrib.auth.decorators import permission_required

@permission_required("accounts.subscription", raise_exception=True)
@staff_member_required
def driver_requests_list(request):
    search_query = request.GET.get('search', '')
    drivers = Driver.objects.filter(Q(enabled=False)&
        (Q(fullName__icontains=search_query) |
        Q(phone__icontains=search_query) |
        Q(email__icontains=search_query))
    )
    return render(request, 'subscription_requests/driver/list.html', {'drivers': drivers, 'search_query': search_query})

@permission_required("accounts.subscription", raise_exception=True)
@staff_member_required
def driver_requests_drtails(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    return render(request, 'subscription_requests/driver/details.html', {'driver': driver})

@permission_required("accounts.subscription", raise_exception=True)
@staff_member_required
def driver_accept_request(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    driver.enabled=True
    driver.save()
    NotificationsHelper.sendRegistrationUpdate(RegistrationUpdate.REGISTR_ACCEPTED,target=driver)
    return redirect('driver_requests_list')

@permission_required("accounts.subscription", raise_exception=True)
@staff_member_required
def driver_reject_request(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    NotificationsHelper.sendRegistrationUpdate(RegistrationUpdate.REGISTR_REJECTED,target=driver)
    driver.delete()
    return redirect('driver_requests_list')
