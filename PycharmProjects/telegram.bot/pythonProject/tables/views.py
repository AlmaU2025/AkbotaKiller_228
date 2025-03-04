from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Table

def table_create(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        seats = request.POST.get('seats')
        table = Table.objects.create(number=number, seats=seats)
        return redirect('table_list')
    return render(request, 'tables/table_form.html')

def table_list(request):
    tables = Table.objects.all()
    return render(request, 'tables/table_list.html', {'tables': tables})

def available_tables(request):
    date = request.GET.get('date')
    if date:
        tables = Table.objects.filter(is_available=True)
    else:
        tables = []
    return render(request, 'tables/available_tables.html', {'tables': tables, 'date': date})

# Create your views here.
