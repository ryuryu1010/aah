# employee_management/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.emprole == 0:
                return redirect('admin_home')
            elif user.emprole == 1:
                return redirect('reception_home')
            elif user.emprole == 2:
                return redirect('doctor_home')
        return render(request, 'login/login.html', {'error': 'Invalid credentials'})


def admin_home(request):
    return render(request, 'index/a_index.html')


def reception_home(request):
    return render(request, 'index/r_index.html')


def doctor_home(request):
    return render(request, 'index/d_index.html')
