from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from ..forms.advertisement import AdvertisementForm
from ..models import Advertisement
from utils.decerators import staff_member_required
from django.contrib.auth.decorators import permission_required

# List all advertisements
@permission_required("accounts.Ads", raise_exception=True)
@staff_member_required
def advertisement_list(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'advertisement/list.html', {'advertisements': advertisements})

# Create a new advertisement
@permission_required("accounts.Ads", raise_exception=True)
@staff_member_required
def advertisement_create(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'advertisement/create.html', {'form': form})

# Update an existing advertisement
@permission_required("accounts.Ads", raise_exception=True)
@staff_member_required
def advertisement_update(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        if form.is_valid():
            form.save()
            return redirect('advertisement_list')
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'advertisement/update.html', {'form': form,'advertisement':advertisement})

# Delete an advertisement
@permission_required("accounts.Ads", raise_exception=True)
@staff_member_required
def advertisement_delete(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    advertisement.delete()
    return redirect('advertisement_list')

