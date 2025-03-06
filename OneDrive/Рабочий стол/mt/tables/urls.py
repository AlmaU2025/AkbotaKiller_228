from django.urls import path
from . import views

urlpatterns = [
    path('', views.table_list, name='table_list'),            # GET /tables/
    path('create/', views.table_create, name='table_create'), # POST /tables/
    path('available/', views.table_available, name='table_available'), # GET /tables/available/
]
