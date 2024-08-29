from django.shortcuts import render,redirect
from ...forms.config.app import AppConfigForm
from ...models import AppConfig
def edit_app_config(request):
    if request.method == 'POST':
        app_config=AppConfig.objects.first()
        form = AppConfigForm(request.POST,instance=app_config)
        if form.is_valid():
            form.save()
            # Redirect to a success page or render a success message
            return redirect('edit_app_config')
    else:
        app_config=AppConfig.objects.first()
        form = AppConfigForm(instance=app_config)
    
    return render(request, 'config/app.html', {'form': form})