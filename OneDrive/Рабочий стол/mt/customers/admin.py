from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')  # Какие поля хотим видеть в списке
    search_fields = ('name', 'phone') # Поля для поиска
