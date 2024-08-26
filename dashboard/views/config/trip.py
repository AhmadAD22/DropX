from django.shortcuts import render, redirect, get_object_or_404
from order.models import TripCar
from accounts.models import CarCategory
from ...forms.config.trip import TripCarForm

def trip_car_list(request):
    trip_cars = CarCategory.objects.all()
    return render(request, 'config/trip/list.html', {'trip_cars': trip_cars})

def add_trip_car(request):
    if request.method == 'POST':
        form = TripCarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trip_car_list')
    else:
        form = TripCarForm()
    return render(request, 'config/trip/add.html', {'form': form})

def update_trip_car(request, pk):
    trip_car = get_object_or_404(CarCategory, pk=pk)
    if request.method == 'POST':
        form = TripCarForm(request.POST, request.FILES, instance=trip_car)
        if form.is_valid():
            form.save()
            return redirect('trip_car_list')
    else:
        form = TripCarForm(instance=trip_car)
    return render(request, 'config/trip/update.html', {'form': form,'trip_car':trip_car})

def delete_trip_car(request, pk):
    trip_car = get_object_or_404(CarCategory, pk=pk)
    trip_car.delete()
    return redirect('trip_car_list')
