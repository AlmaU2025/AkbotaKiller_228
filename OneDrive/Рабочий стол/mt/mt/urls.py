# mt/urls.py
from django.contrib import admin
from django.urls import path, include
# Импортируем свой view-функцию (создадим ниже)
from . import views

urlpatterns = [
    path('', views.index, name='home'),          # <-- добавим это
    path('admin/', admin.site.urls),
    path('customers/', include('customers.urls')),
    path('tables/', include('tables.urls')),
    path('reservations/', include('reservations.urls')),
]
