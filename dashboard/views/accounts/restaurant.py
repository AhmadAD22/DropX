from django.shortcuts import render, redirect,get_object_or_404
from ...forms.accounts.restaurant import RestaurantForm
from accounts.models import Restaurant,RestaurantSubscription
from django.db.models import Q


def create_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')  # Redirect to a success page
    else:
        form = RestaurantForm()
    return render(request, 'create_restaurant.html', {'form': form})

def restaurant_list(request):
    search_query = request.GET.get('search','')
    restaurants = Restaurant.objects.filter(Q(enabled=True)&
        Q(restaurantName__icontains=search_query) |
        Q(phone__icontains=search_query) |
        Q(email__icontains=search_query)
    )
    return render(request, 'accounts/restaurant/list.html', {'restaurants': restaurants, 'search_query': search_query})

def update_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')  # Redirect to a success page
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'accounts/restaurant/update.html', {'form': form,'restaurant':restaurant})

def restaurant_delete(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurant_list')
    
    
def restaurant_subscription(request, pk):
    restaurant = get_object_or_404(Restaurant,pk=pk)
    restaurant_subscriptions=RestaurantSubscription.objects.filter(restaurant=restaurant)
    return render(request, 'accounts/restaurant/subscription.html', {'restaurant':restaurant,'restaurant_subscriptions':restaurant_subscriptions})
    
def restaurant_order_subscription_disable(request, pk):
    restaurant = get_object_or_404(Restaurant,pk=pk)
    restaurant_subscriptions=RestaurantSubscription.objects.filter(restaurant=restaurant)
    if restaurant_subscriptions:
        for subscription in restaurant_subscriptions:
            subscription.enabled=False
            subscription.save()
            print(subscription.enabled)
    return redirect('restaurant_subscription',pk)

def restaurant_order_subscription_enable(request, pk):
    restaurant = get_object_or_404(Restaurant,pk=pk)
    restaurant_subscriptions=RestaurantSubscription.objects.filter(restaurant=restaurant)
    if restaurant_subscriptions:
        for subscription in restaurant_subscriptions:
            subscription.enabled=True
            subscription.save()
            print(subscription.enabled)
    return redirect('restaurant_subscription',pk)


    