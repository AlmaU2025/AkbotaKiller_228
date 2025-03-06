# mt/views.py
from django.shortcuts import redirect

def index(request):
    # Например, сразу перенаправим на список клиентов:
    return redirect('customer_list')
    # Или отрендерим шаблон главной страницы
    # return render(request, 'index.html')
