from django.shortcuts import render, redirect
from order.models import OrderConfig
from ...forms.config.order import OrderConfigForm
from utils.decerators import staff_member_required
from django.contrib.auth.decorators import permission_required



@permission_required("accounts.config", raise_exception=True)
@staff_member_required
def order_config_view(request):
    order_config = OrderConfig.objects.first()
    
    if request.method == 'POST':
        form = OrderConfigForm(request.POST, instance=order_config)
        if form.is_valid():
            form.save()
            return redirect('order_config_view')
    else:
        form = OrderConfigForm(instance=order_config)
    
    return render(request, 'config/order_config.html', {'form': form})