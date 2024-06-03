from datetime import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee, Shiiregyosha, Patient, Treatment, Medicine
from datetime import datetime
from django.utils import timezone
from urllib.parse import urlencode


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


def a_index(request):
    return render(request, '../templates//index/a_index.html')


def r_index(request):
    return render(request, '../templates//index/r_index.html')


def d_index(request):
    return render(request, '../templates//index/d_index.html')


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
            return render(request, '../templates/administrar/E101/error.html',
                          {'error_message': 'Passwords do not match.'})

        if Employee.objects.filter(empid=empid).exists():
            messages.error(request, 'Employee ID already exists.')
            return render(request, '../templates/administrar/E101/error.html',
                          {'error_message': 'Passwords do not match.'})

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


def Add_vendor(request):
    if request.method == 'POST':
        shiireid = request.POST['shiireid']
        shiiremei = request.POST['shiiremei']
        shiireaddress = request.POST['shiireaddress']
        shiiretel = request.POST['shiiretel']
        shihonkin = request.POST['shihonkin']
        nouki = request.POST['nouki']

        if Shiiregyosha.objects.filter(shiireid=shiireid).exists():
            return render(request, '../templates/administrar/S101/error.html',
                          {'error_message': 'Supplier ID already exists.'})

        supplier = Shiiregyosha(
            shiireid=shiireid,
            shiiremei=shiiremei,
            shiireaddress=shiireaddress,
            shiiretel=shiiretel,
            shihonkin=shihonkin,
            nouki=nouki
        )
        supplier.save()
        messages.success(request, 'Supplier registered successfully.')
        return redirect('supplier_TBL')

    return render(request, '../templates/administrar/S101/Ability_to_add_records.html')


def supplier_TBL(request):
    suppliers = Shiiregyosha.objects.all()
    return render(request, '../templates/administrar/S102/Supplier _TBL.html', {'suppliers': suppliers})


def address_search(request):
    if request.method == 'GET':
        return render(request, '../templates/administrar/S103/Housing_search.html')

    if request.method == 'POST':
        address_search = request.POST.get('address_search', '')
        if address_search:
            results = Shiiregyosha.objects.filter(shiireaddress__icontains=address_search)
            if results.exists():
                return render(request, '../templates/administrar/S103/Housing_search.html', {'results': results})
            else:
                messages.error(request, '一致する仕入れ先が見つかりませんでした。')
                return render(request, '../templates/administrar/S103/Housing_search.html')
        else:
            messages.error(request, '住所を入力してください。')
            return render(request, '../templates/administrar/S103/Housing_search.html')


def change_password(request):
    if request.method == 'POST':
        empid = request.POST['employee_id']
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        try:
            employee = Employee.objects.get(empid=empid, emppasswd=current_password)
        except Employee.DoesNotExist:
            messages.error(request, '従業員IDまたは現在のパスワードが正しくありません。')
            return render(request, 'administrar/E103/password_change_error.html')

        if employee.emprole == 0:
            messages.error(request, '管理者のパスワードは変更できません。')
            return render(request, 'administrar/E103/password_change_error.html')

        if new_password != confirm_new_password:
            messages.error(request, '新しいパスワードが一致しません。')
            return render(request, 'administrar/E103/password_change_error.html')

        employee.emppasswd = new_password
        employee.save()
        messages.success(request, 'パスワードが正常に変更されました。')
        return redirect('password_change_success')

    emprole = request.session.get('emp_role')
    context = {'emprole': emprole}
    return render(request, 'administrar/E103/Employee_password_change.html', context)


def password_change_success(request):
    return render(request, 'administrar/E103/password_change_success.html')


def patient_registration(request):
    if request.method == 'POST':
        patient_id = request.POST['patid']
        last_name = request.POST['patfname']
        first_name = request.POST['patiname']
        insurance_number = request.POST['hokenmei']
        expiration_date = request.POST['hokenexp']

        if not all([patient_id, last_name, first_name, insurance_number, expiration_date]):
            messages.error(request, '全ての項目を入力してください。')
            return render(request, '../templates/reception/P101/patient_registration_error.html',
                          {'error_message': '全ての項目を入力してください。'})

        if Patient.objects.filter(patid=patient_id).exists():
            messages.error(request, '患者IDが既に存在します。')
            return render(request, '../templates/reception/P101/patient_registration_error.html',
                          {'error_message': '患者IDが既に存在します。'})

        patient = Patient(
            patid=patient_id,
            patfname=first_name,
            patiname=last_name,
            hokenmei=insurance_number,
            hokenexp=expiration_date
        )
        patient.save()

        messages.success(request, '患者が正常に登録されました。')
        return redirect('patient_registration_success')

    return render(request, '../templates/reception/P101/Patient_registration.html')


def patient_registration_success(request):
    return render(request, '../templates/reception/P101/patient_registration_succes.html')


def patient_insurance_change_success(request):
    return render(request, '../templates/reception/P102/patient_insurance_change_success.html')


def patient_list(request):
    patients = Patient.objects.all()
    return render(request, '../templates/reception/P102/patient_list.html', {'patients': patients})


def edit_patient_insurance(request, patid):
    patient = get_object_or_404(Patient, patid=patid)

    if request.method == 'POST':
        insurance_number = request.POST['insurance_number']
        expiration_date = request.POST['expiration_date']

        if insurance_number:
            patient.hokenmei = insurance_number

        if expiration_date:
            patient.hokenexp = expiration_date

        patient.save()
        messages.success(request, '保険証情報が正常に変更されました。')
        return redirect('patient_list')

    return render(request, 'reception/P102/edit_patient_insurance.html', {'patient': patient})


def search_patients(request):
    patients = []
    expiration_date_str = request.GET.get('expiration_date')
    if expiration_date_str:
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
        patients = Patient.objects.filter(hokenexp__lt=expiration_date)
    else:
        patients = Patient.objects.all()

    emprole = request.session.get('emp_role', None)

    context = {
        'patients': patients,
        'emprole': emprole,
    }
    return render(request, 'reception/P104/Patient_search.html', context)


def add_treatment(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        doctor_id = request.session.get('userID')  # セッションから医師IDを取得
        medicine_id = request.POST.get('medicine_id')
        quantity = request.POST.get('quantity')

        patient = get_object_or_404(Patient, pk=patient_id)
        doctor = get_object_or_404(Employee, pk=doctor_id)
        medicine = get_object_or_404(Medicine, pk=medicine_id)

        treatment = Treatment(patient=patient, doctor=doctor, medicine=medicine, quantity=quantity)
        treatment.save()

        return redirect('confirm_treatment', treatment_id=treatment.treatmentid)

    patients = Patient.objects.all()
    medicines = Medicine.objects.all()
    context = {
        'patients': patients,
        'medicines': medicines
    }
    return render(request, '../templates/doctor/D101/add_treatment.html', context)





def treatment_success(request):
    return render(request, '../templates/doctor/D101/treatment_success.html')



def decrease_treatment_quantity(request, treatment_id):
    treatment = get_object_or_404(Treatment, treatmentid=treatment_id)
    if request.method == 'POST':
        decrement_value = int(request.POST.get('decrement_value'))
        if decrement_value > treatment.quantity:
            # エラーメッセージを表示
            context = {'treatment': treatment, 'error': '減少する数量が現在の数量を超えています。'}
            return render(request, 'doctor/D102/decrease_treatment_quantity.html', context)
        else:
            treatment.quantity -= decrement_value
            treatment.save()
            return redirect('confirm_treatment', treatment_id=treatment.treatmentid)
    return render(request, 'doctor/D102/decrease_treatment_quantity.html', {'treatment': treatment})


def treatment_deleted(request):
    return render(request, '../templates/doctor/D102/treatment_deleted.html')


















def confirm_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, pk=treatment_id)

    if request.method == 'POST':
        treatment.confirmed = True
        treatment.save()
        messages.success(request, '処置が正常に確定されました。')
        return redirect('treatment_success')

    context = {
        'treatment': treatment
    }
    return render(request, '../templates/doctor/D103/confirm_treatment.html', context)




def treatment_history(request):
    patient = None
    patients = None
    treatments = None

    if request.method == 'POST':
        if 'patid_search' in request.POST:
            patid = request.POST.get('patid')
            if patid:
                if Patient.objects.filter(patid=patid).exists():
                    patient = get_object_or_404(Patient, patid=patid)
                    treatments = Treatment.objects.filter(patient=patient)
                else:
                    return redirect('error_page', error_message='該当する患者が見つかりません。')
        elif 'all_patients' in request.POST:
            patients = Patient.objects.all()
            treatments = Treatment.objects.all()

    context = {
        'patient': patient,
        'patients': patients,
        'treatments': treatments,
    }

    return render(request, '../templates/doctor/D104/treatment_history.html', context)




def error_page(request):
    error_message = request.GET.get('error_message', 'エラーが発生しました。')
    return render(request, '../templates/error/error_page.html', {'error_message': error_message})
