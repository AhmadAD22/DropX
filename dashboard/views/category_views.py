from django.shortcuts import render,redirect,get_object_or_404
from restaurant.models import Category
from ..forms.category_form import *

def category_list(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'category/categories_list.html',context=context)
    

# عرض لإضافة فئة جديدة
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/create.html', {'form': form})


def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/update.html', {'form': form})

# # عرض لحذف فئة
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    