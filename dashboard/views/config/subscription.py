from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import SubscriptionConfig
from ...forms.config.subscription import SubscriptionConfigForm
from utils.decerators import staff_member_required
from django.contrib.auth.decorators import permission_required



@permission_required("accounts.config", raise_exception=True)
@staff_member_required
def subscription_config_list(request):
    subscription_config=SubscriptionConfig.objects.all()
    member_subscriptions=subscription_config.filter(type="MEMBERS")
    order_subscriptions=subscription_config.filter(type="ORDERS")
    restaurant_subscriptions=subscription_config.filter(type="RESTAURANT")
    return render(request, 'config/subscription/list.html',
                  {'member_subscriptions': member_subscriptions,
                   'order_subscriptions':order_subscriptions,
                    'restaurant_subscriptions':restaurant_subscriptions})
    
@permission_required("accounts.config", raise_exception=True)
@staff_member_required
def update_subscription_config(request,pk):
    subscription_config = get_object_or_404(SubscriptionConfig, id=pk)

    if request.method == 'POST':
        form = SubscriptionConfigForm(request.POST, instance=subscription_config)
        if form.is_valid():
            form.save()
            return redirect('subscription_config_list')  # Adjust the URL name as needed
    else:
        form = SubscriptionConfigForm(instance=subscription_config)

    return render(request, 'config/subscription/update.html', {'form': form, 'subscription_config': subscription_config})