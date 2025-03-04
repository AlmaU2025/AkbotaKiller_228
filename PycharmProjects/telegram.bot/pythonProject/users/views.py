from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'users/user_detail.html', {'user': user})

def user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Можно добавить дополнительные поля, валидацию и обработку ошибок
        user = User.objects.create_user(username=username, password=password)
        return redirect('user_detail', id=user.id)
    return render(request, 'users/user_form.html')
