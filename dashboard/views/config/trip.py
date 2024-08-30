from django.shortcuts import render, redirect, get_object_or_404
from order.models import TripCar
from accounts.models import CarCategory,Car
from ...forms.config.trip import TripCarForm,CarForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def trip_car_list(request):
    trip_cars = CarCategory.objects.all().order_by('id')  # Order the queryset by a field (e.g., 'id')
    paginator = Paginator(trip_cars, 5)  # Show 5 trip cars per page

    page = request.GET.get('page')
    try:
        trip_cars = paginator.page(page)
    except PageNotAnInteger:
        trip_cars = paginator.page(1)
    except EmptyPage:
        trip_cars = paginator.page(paginator.num_pages)
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


#Car Type Config


def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')  # Redirect to a view that lists cars
    else:
        form = CarForm()
    
    return render(request, 'config/cars/add.html', {'form': form})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def car_list(request):
    car_list = Car.objects.order_by('id')  # Explicitly order the queryset by a field (e.g., 'id')
    paginator = Paginator(car_list, 7)  # Show 5 cars per page

    page = request.GET.get('page')
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)
    num_pages = paginator.num_pages
    return render(request, 'config/cars/list.html', {'cars': cars,'num_pages':num_pages})

def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    return redirect('car_list')