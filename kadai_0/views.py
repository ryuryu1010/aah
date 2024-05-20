# employee_management/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from .models import Employee


def login(request):
    if request.method == "GET":
        return render(request,'../templates/login/login.html')

    if request.method == "POST":
        userID = request.POST['userID']
        password = request.POST['password']
        request.session['userID'] = userID

    try:
        emp_info = Employee.objects.get(empid=userID,emppasswd=password)
        request.session['emp_role'] = emp_info.emprole

        if emp_info.emprole == 0:
            return render(request, '../templates/index/a_index.html')
        elif emp_info.emprole == 1:
            return render(request, '../templates/index/d_index.html')
        elif emp_info.emprole == 2:
            return render(request, '../templates/index/r_index.html')

    except Employee.DoesNotExist:
        return render(request, '../templates/login/login_error.html')

def logout(request):
    logout(request)
    return render(request, '../templates/logout/logout.html')

