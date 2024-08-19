from django.shortcuts import render, redirect,get_object_or_404
from restaurant.models import Product, AccessoryProduct
from ...forms.products import ProductForm, AccessoryProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from accounts.models import Restaurant

def product_list(request,restaurant_id):
    search_query = request.GET.get('search','')
    products = Product.objects.filter(Q(restaurant__id=restaurant_id)&
    (Q(name__icontains=search_query) |
        Q(price__icontains=search_query) |
        Q(offers__icontains=search_query)|
         Q(category__name__icontains=search_query)) )

    restaurant=get_object_or_404(Restaurant,pk=restaurant_id)
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 5)  # Show 10 products per page
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'accounts/restaurant/products/list.html', {'products': products,'restaurant':restaurant,'search_query': search_query})

def add_product(request,restaurant_id):
    restaurant=get_object_or_404(Restaurant,pk=restaurant_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product=form.save(commit=False)
            product.restaurant=restaurant
            product.save()
            return redirect('product_list',restaurant_id)
    else:
        form = ProductForm()
    return render(request, 'accounts/restaurant/products/add.html', {'form': form,'restaurant':restaurant})

def update_product(request, restaurant_id, product_id=None):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    product = None

    if product_id:
        product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.restaurant = restaurant
            product.save()
            return redirect('product_list', restaurant_id)
    else:
        form = ProductForm(instance=product)
    accessorys=AccessoryProduct.objects.filter(product=product)
    return render(request, 'accounts/restaurant/products/update.html', {'form': form, 'restaurant': restaurant, 'product': product,'accessorys':accessorys})

def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()
    return redirect('product_list',product.restaurant.id)

def add_accessory_product(request,restaurant_id, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = AccessoryProductForm(request.POST)
        if form.is_valid():
            accessory_product = form.save(commit=False)
            accessory_product.product = product
            accessory_product.save()
            return redirect('update_product',restaurant_id,product_id)
    else:
        form = AccessoryProductForm()
    return render(request, 'accounts/restaurant/products/accessory/add.html', {'form': form, 'product': product,'restaurant':product.restaurant,})

def update_accessory_product(request, restaurant_id, product_id, accessory_product_id):
    product = get_object_or_404(Product, id=product_id)
    accessory_product = get_object_or_404(AccessoryProduct, id=accessory_product_id)
    if request.method == 'POST':
        form = AccessoryProductForm(request.POST, instance=accessory_product)
        if form.is_valid():
            form.save()
            return redirect('update_product',restaurant_id,product_id)
    else:
        form = AccessoryProductForm(instance=accessory_product)

    return render(request, 'accounts/restaurant/products/accessory/update.html', {'form': form, 'product': product, 'accessory_product': accessory_product, 'restaurant': product.restaurant})

def delete_accessory_product(request, pk):
    accessory_product = get_object_or_404(AccessoryProduct, id=pk)
    product=accessory_product.product
    accessory_product.delete()
    return redirect('update_product',product.restaurant.id,product.id)
    