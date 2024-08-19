from django.shortcuts import render, redirect,get_object_or_404
from ...forms.accounts.admin import UserCreationWithPermissionsForm,User,UserUpdateForm
from django.db.models import Q
from django.contrib import messages


def admin_list(request):
    search_query = request.GET.get('search', '')
    admins = User.objects.filter(Q(is_staff=True)&(
        Q(fullName__icontains=search_query) |
        Q(phone__icontains=search_query) |
        Q(email__icontains=search_query))
    )
    return render(request, 'accounts/admin/list.html', {'admins': admins, 'search_query': search_query})

def add_user_with_permissions(request):
    if request.method == 'POST':
        form = UserCreationWithPermissionsForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("admin_list") # Redirect to a success page
    else:
        form = UserCreationWithPermissionsForm()
    
    return render(request, 'accounts/admin/add_user_with_permissions.html', {'form': form})



from django.contrib.auth.models import Permission

def update_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            # Save the form to update the user details
            updated_user = form.save(commit=False)
            
            # Update the user's permissions based on the selected permissions in the form
            selected_permissions = form.cleaned_data['permissions']
            updated_user.user_permissions.set(selected_permissions)
            
            updated_user.save()
            
            return redirect('admin_list')  # Redirect to a success page
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'accounts/admin/update.html', {'form': form, 'user': user})

def delete_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_list')
    
def change_password(request, user_id):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()
       
        return redirect('update_admin', user.id)  # Redirect to a success page