from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),          # GET /customers/
    path('create/', views.customer_create, name='customer_create'),# POST /customers/
    path('<int:customer_id>/', views.customer_detail, name='customer_detail'),  # GET /customers/{id}/
]
