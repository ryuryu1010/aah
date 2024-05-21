from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee

def login(request):
    if request.method == "GET":
        return render(request, '../templates/login/login.html')

    if request.method == "POST":
        userID = request.POST['userID']
        password = request.POST['password']
        request.session['userID'] = userID

        try:
            emp_info = Employee.objects.get(empid=userID, emppasswd=password)
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
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return render(request, '../templates/logout/logout.html')

def employee_registration(request):
    if request.method == 'POST':
        empid = request.POST['empid']
        empfname = request.POST['empfname']
        empiname = request.POST['empiname']
        emppasswd1 = request.POST['emppasswd1']
        emppasswd2 = request.POST['emppasswd2']
        emprole = request.POST['emprole']

        if emppasswd1 != emppasswd2:
            messages.error(request, 'Passwords do not match.')
            return render(request, '../templates/administrar/E101/error.html', {'error_message': 'Passwords do not match.'})

        if Employee.objects.filter(empid=empid).exists():
            messages.error(request, 'Employee ID already exists.')
            return render(request, '../templates/administrar/E101/error.html', {'error_message': 'Passwords do not match.'})

        employee = Employee(
            empid=empid,
            empfname=empfname,
            empiname=empiname,
            emppasswd=emppasswd1,  # パスワードをそのまま保存
            emprole=emprole
        )
        employee.save()
        messages.success(request, 'Employee registered successfully.')
        return redirect('employee_list')  # 適切なリダイレクト先に変更してください

    return render(request, '../templates/administrar/E101/Current _employee_registration_function.html')

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, '../templates/administrar/E101/employee_list.html', {'employees': employees})
