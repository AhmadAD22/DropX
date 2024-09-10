from django.shortcuts import render,redirect,get_object_or_404
from restaurant.models import Category
from ..forms.category_form import *
from utils.decerators import *
from django.contrib.auth.decorators import permission_required



@permission_required("accounts.Categories", raise_exception=True)
@staff_member_required
def category_list(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'category/categories_list.html',context=context)
    

@permission_required("accounts.Categories", raise_exception=True)
@staff_member_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category/create.html', {'form': form})

@permission_required("accounts.Categories", raise_exception=True)
@staff_member_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/update.html', {'form': form,'category':category})

@permission_required("accounts.Categories", raise_exception=True)
@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    