from django.shortcuts import render, redirect,get_object_or_404
from accounts.models import Restaurant
from django.db.models import Q
from utils.notifications import *

def restaurant_requests_list(request):
    search_query = request.GET.get('search', '')
    restaurants = Restaurant.objects.filter(Q(enabled=False)&
        (Q(restaurantName__icontains=search_query) |
        Q(phone__icontains=search_query) |
        Q(email__icontains=search_query))
    )
    return render(request, 'subscription_requests/restaurant/list.html', {'restaurants': restaurants, 'search_query': search_query})


def restaurant_requests_details(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'subscription_requests/restaurant/details.html', {'restaurant': restaurant})

def restaurant_accept_request(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    restaurant.enabled=True
    restaurant.save()
    NotificationsHelper.sendRegistrationUpdate(RegistrationUpdate.REGISTR_ACCEPTED,target=restaurant)
    return redirect('restaurant_requests_list')

def restaurant_reject_request(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    NotificationsHelper.sendRegistrationUpdate(RegistrationUpdate.REGISTR_REJECTED,target=restaurant)
    restaurant.delete()
    return redirect('restaurant_requests_list')
