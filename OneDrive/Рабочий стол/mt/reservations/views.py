from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from datetime import datetime

from .models import Reservation
from customers.models import Customer
from tables.models import Table

def reservation_create(request):
    """
    GET /reservations/ -> Показать форму, список броней, список клиентов, список столов.
    POST /reservations/ -> Создать бронь.
    """
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        table_id = request.POST.get('table_id')
        date_str = request.POST.get('date')  # поддерживаем форматы YYYY-MM-DD и DD.MM.YYYY

        # 1. Проверка, что данные есть
        if not (customer_id and table_id and date_str):
            return HttpResponse("Недостаточно данных (укажите customer_id, table_id, date).", status=400)

        # 2. Проверка существования клиента
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return HttpResponse(f"Клиент с id={customer_id} не найден.", status=400)

        # 3. Проверка существования стола
        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            return HttpResponse(f"Стол с id={table_id} не найден.", status=400)

        # 4. Парсим дату (два формата)
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, '%d.%m.%Y').date()
            except ValueError:
                return HttpResponse("Неверный формат даты. Используйте YYYY-MM-DD или DD.MM.YYYY.", status=400)

        # 5. Проверка: нет ли уже брони у этого пользователя на этот день
        if Reservation.objects.filter(customer=customer, date=date_obj).exists():
            return HttpResponse("У пользователя уже есть бронь на эту дату.", status=400)

        # 6. Проверка: не занят ли стол на эту дату
        if Reservation.objects.filter(table=table, date=date_obj).exists():
            return HttpResponse("Стол уже забронирован на эту дату.", status=400)

        # 7. Создаём бронь
        Reservation.objects.create(
            customer=customer,
            table=table,
            date=date_obj,
            status='pending'
        )

        # 8. Перенаправляем на GET /reservations/, чтобы показать форму + обновленный список
        return redirect('reservation_create')

    else:
        # GET-запрос: показываем форму + список всех бронирований + список клиентов и столов
        all_reservations = Reservation.objects.all().order_by('-id')
        all_customers = Customer.objects.all().order_by('name')
        all_tables = Table.objects.all().order_by('number')

        return render(request, 'reservations/reservation_create_form.html', {
            'reservations': all_reservations,
            'customers': all_customers,
            'tables': all_tables,
        })


def reservation_detail(request, reservation_id):
    """
    GET /reservations/{id}/ – получить детали конкретной брони
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservations/reservation_detail.html', {'reservation': reservation})


def user_reservations(request, user_id):
    """
    GET /reservations/user/{user_id}/ – список всех броней конкретного пользователя
    """
    customer = get_object_or_404(Customer, id=user_id)
    reservations = Reservation.objects.filter(customer=customer)
    return render(request, 'reservations/user_reservations.html', {
        'reservations': reservations,
        'customer': customer
    })


def reservation_update(request, reservation_id):
    """
    POST /reservations/{id}/update/ – обновить статус брони (подтвердить, отменить и т.д.)
    """
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'canceled']:
            reservation.status = new_status
            reservation.save()
            return redirect('reservation_detail', reservation_id=reservation.id)
        else:
            return HttpResponse("Неподдерживаемый статус.", status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


def reservation_delete(request, reservation_id):
    """
    POST /reservations/{id}/delete/ – удалить бронь
    """
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        reservation.delete()
        return redirect('reservation_create')  # возвращаемся к общему списку
    else:
        return HttpResponseNotAllowed(['POST'])
