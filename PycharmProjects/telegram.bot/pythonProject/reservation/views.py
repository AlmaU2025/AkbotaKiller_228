from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation
from tables.models import Table
from django.contrib.auth.models import User


def reservation_create(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        table_id = request.POST.get('table_id')
        res_date = request.POST.get('date')
        user = get_object_or_404(User, id=user_id)
        table = get_object_or_404(Table, id=table_id)

        if Reservation.objects.filter(table=table, date=res_date).exists():
            return render(request, 'reservations/reservation_error.html', {
                'message': 'Столик уже забронирован на эту дату'
            })

        if Reservation.objects.filter(user=user, date=res_date).exists():
            return render(request, 'reservations/reservation_error.html', {
                'message': 'У пользователя уже есть бронь на этот день'
            })

        reservation = Reservation.objects.create(user=user, table=table, date=res_date, status='pending')
        return redirect('reservation_detail', id=reservation.id)
    # Если GET – вывод формы для создания брони
    return render(request, 'reservations/reservation_form.html')


def reservation_detail(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    return render(request, 'reservations/reservation_detail.html', {'reservation': reservation})


def reservations_by_user(request, user_id):
    reservations = Reservation.objects.filter(user__id=user_id)
    return render(request, 'reservations/reservations_by_user.html', {'reservations': reservations})


def reservation_update(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Reservation.STATUS_CHOICES).keys():
            reservation.status = new_status
            reservation.save()
            return redirect('reservation_detail', id=reservation.id)
    return render(request, 'reservations/reservation_update.html', {'reservation': reservation})


def reservation_delete(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    if request.method == 'POST':
        user_id = reservation.user.id
        reservation.delete()
        return redirect('reservations_by_user', user_id=user_id)
    return render(request, 'reservations/reservation_confirm_delete.html', {'reservation': reservation})

# Create your views here.
