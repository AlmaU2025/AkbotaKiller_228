from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_create, name='reservation_create'),                  # POST /reservations/
    path('<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),  # GET /reservations/{id}/
    path('user/<int:user_id>/', views.user_reservations, name='user_reservations'),     # GET /reservations/user/{user_id}/
    path('<int:reservation_id>/update/', views.reservation_update, name='reservation_update'),  # POST /reservations/{id}/
    path('<int:reservation_id>/delete/', views.reservation_delete, name='reservation_delete'),  # DELETE /reservations/{id}/
]
