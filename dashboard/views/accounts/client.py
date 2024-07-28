from django.shortcuts import render, redirect
from ...forms.accounts.client_forms import ClientForm
from accounts.models import Client
from django.db.models import Q

def client_list(request):
    search_query = request.GET.get('search', '')
    clients = Client.objects.filter(
        Q(fullName__icontains=search_query) |
        Q(phone__icontains=search_query) |
        Q(email__icontains=search_query)
    )
    return render(request, 'accounts/client/client_list.html', {'clients': clients, 'search_query': search_query})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'client_create.html', {'form': form})

def client_update(request, pk):
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'accounts/client/client_update.html', {'form': form,'client_id':client.id})

def client_delete(request, pk):
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'client_delete.html', {'client': client})