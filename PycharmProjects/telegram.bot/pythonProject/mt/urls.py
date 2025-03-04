from django.contrib import admin
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users.urls")),
    path('tables/', include("tables.urls")),
    path('reservations/', include('reservation.urls')),
]
