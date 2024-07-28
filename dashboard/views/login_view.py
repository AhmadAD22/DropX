from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login,logout




def login_view(request):
    if request.user.is_authenticated:
        return redirect("main_dashboard")
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
            return redirect("main_dashboard")
        else:
            error_message = 'Invalid phone number or password'
            return render(request, 'login/login.html', {'error_message': error_message})
    else:
        return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect('dashboard-login')