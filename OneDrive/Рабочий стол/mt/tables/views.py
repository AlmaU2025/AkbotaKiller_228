from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Table
from datetime import datetime
from reservations.models import Reservation

def table_list(request):
    """
    GET /tables/ – получить список всех столов (через шаблон)
    """
    if request.method == 'GET':
        tables = Table.objects.all()
        return render(request, 'tables/tables_list.html', {'tables': tables})

def table_create(request):
    """
    POST /tables/ – создать столик
    """
    if request.method == 'POST':
        number = request.POST.get('number')
        seats = request.POST.get('seats')

        # Проверка на пустые данные
        if not number or not seats:
            return HttpResponse("Нужно указать номер стола и количество мест.", status=400)

        # Проверка, не существует ли уже стол с таким же номером
        if Table.objects.filter(number=number).exists():
            return HttpResponse("Стол с таким номером уже существует!", status=400)

        # Если всё в порядке — создаём стол
        Table.objects.create(number=number, seats=seats)
        return redirect('table_list')
    else:
        # Если GET, выводим форму создания
        return render(request, 'tables/table_create_form.html')

def table_available(request):
    """
    GET /tables/available/?date=YYYY-MM-DD
    Возвращает список доступных столиков на указанную дату.
    """
    date_str = request.GET.get('date')

    if date_str:
        # Парсим дату из строки 'YYYY-MM-DD'
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            # Если не удалось распарсить, вернём пустой список или ошибку
            return HttpResponse("Неверный формат даты, используйте YYYY-MM-DD.", status=400)

        # Ищем столы, которые уже заняты на указанную дату
        reserved_tables = Reservation.objects.filter(date=date_obj).values_list('table_id', flat=True)

        # Исключаем занятые столы из общего списка
        available_tables = Table.objects.exclude(id__in=reserved_tables)
    else:
        # Если дата не указана, вернёт все "is_available=True" (свободные по умолчанию)
        available_tables = Table.objects.filter(is_available=True)
    
    return render(request, 'tables/available_tables.html', {
        'tables': available_tables,
        'date': date_str
    })
