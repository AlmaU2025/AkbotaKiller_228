from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer

def customer_list(request):
    """
    GET /customers/ – получить список всех пользователей.
    Выводим список через шаблон.
    """
    if request.method == 'GET':
        customers = Customer.objects.all()
        return render(request, 'customers/customers_list.html', {'customers': customers})

def customer_create(request):
    """
    POST /customers/ – создать пользователя
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        # Простейшее создание, без форм Django
        customer = Customer.objects.create(name=name, phone=phone)
        return redirect('customer_list')
    else:
        # Если GET, можно отрендерить форму для создания (по желанию)
        return render(request, 'customers/customer_create_form.html')

def customer_detail(request, customer_id):
    """
    GET /customers/{id}/ – получить информацию о пользователе
    """
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'customers/customer_detail.html', {'customer': customer})
