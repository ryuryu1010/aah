from datetime import timezone

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee, Shiiregyosha, Patient, Treatment, Medicine
from datetime import datetime
from django.utils import timezone
from urllib.parse import urlencode

# ログイン処理を行うビュー関数
def login(request):
    if request.method == "GET":
        return render(request, '../templates/login/login.html')  # ログインページを表示

    if request.method == "POST":
        userID = request.POST['userID']  # POSTデータからユーザーIDを取得
        password = request.POST['password']  # POSTデータからパスワードを取得
        request.session['userID'] = userID  # セッションにユーザーIDを保存

        try:
            emp_info = Employee.objects.get(empid=userID, emppasswd=password)  # ユーザーIDとパスワードで従業員情報を取得
            request.session['emp_role'] = emp_info.emprole  # セッションに従業員の役割を保存

            if emp_info.emprole == 0:
                return render(request, '../templates/index/a_index.html')  # 管理者ホーム画面を表示
            elif emp_info.emprole == 1:
                return render(request, '../templates/index/d_index.html')  # 医師ホーム画面を表示
            elif emp_info.emprole == 2:
                return render(request, '../templates/index/r_index.html')  # 受付ホーム画面を表示

        except Employee.DoesNotExist:
            return render(request, '../templates/error/error_page.html', {'error_message': 'ユーザーIDまたはパスワードが間違っています'})  # エラーページを表示

# 管理者ホーム画面を表示するビュー関数
def a_index(request):
    return render(request, '../templates/index/a_index.html')

# 受付ホーム画面を表示するビュー関数
def r_index(request):
    return render(request, '../templates/index/r_index.html')

# 医師ホーム画面を表示するビュー関数
def d_index(request):
    return render(request, '../templates/index/d_index.html')

# ログアウト処理を行うビュー関数
def logout(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)  # ログアウト処理を実行
    return render(request, '../templates/logout/logout.html')  # ログアウトページを表示

# 従業員登録を処理するビュー関数
def employee_registration(request):
    if request.method == 'POST':
        empid = request.POST['empid']  # POSTデータから従業員IDを取得
        empfname = request.POST['empfname']  # POSTデータから従業員の姓を取得
        empiname = request.POST['empiname']  # POSTデータから従業員の名を取得
        emppasswd1 = request.POST['emppasswd1']  # POSTデータからパスワードを取得
        emppasswd2 = request.POST['emppasswd2']  # POSTデータからパスワード確認を取得
        emprole = request.POST['emprole']  # POSTデータから従業員の役割を取得

        if emppasswd1 != emppasswd2:
            messages.error(request, 'Passwords do not match.')  # パスワードが一致しない場合、エラーメッセージを表示
            return render(request, '../templates/error/error_page.html', {'error_message': 'Passwords do not match.'})

        if Employee.objects.filter(empid=empid).exists():
            messages.error(request, 'Employee ID already exists.')  # 従業員IDが既に存在する場合、エラーメッセージを表示
            return render(request, '../templates/error/error_page.html', {'error_message': 'Employee ID already exists.'})

        employee = Employee(
            empid=empid,
            empfname=empfname,
            empiname=empiname,
            emppasswd=emppasswd1,  # パスワードをそのまま保存
            emprole=emprole
        )
        employee.save()  # 従業員情報を保存
        messages.success(request, 'Employee registered successfully.')  # 成功メッセージを表示
        return redirect('employee_list')  # 従業員リストページにリダイレクト

    return render(request, '../templates/administrar/E101/Current _employee_registration_function.html')

# 従業員リストを表示するビュー関数
def employee_list(request):
    employees = Employee.objects.all()  # 全従業員情報を取得
    return render(request, '../templates/administrar/E101/employee_list.html', {'employees': employees})

# 仕入先追加を処理するビュー関数
def Add_vendor(request):
    if request.method == 'POST':
        shiireid = request.POST['shiireid']  # POSTデータから仕入先IDを取得
        shiiremei = request.POST['shiiremei']  # POSTデータから仕入先名を取得
        shiireaddress = request.POST['shiireaddress']  # POSTデータから仕入先住所を取得
        shiiretel = request.POST['shiiretel']  # POSTデータから仕入先電話番号を取得
        shihonkin = request.POST['shihonkin']  # POSTデータから資本金を取得
        nouki = request.POST['nouki']  # POSTデータから納期を取得

        if Shiiregyosha.objects.filter(shiireid=shiireid).exists():
            return render(request, '../templates/error/error_page.html', {'error_message': 'Supplier ID already exists.'})  # 仕入先IDが既に存在する場合、エラーメッセージを表示

        supplier = Shiiregyosha(
            shiireid=shiireid,
            shiiremei=shiiremei,
            shiireaddress=shiireaddress,
            shiiretel=shiiretel,
            shihonkin=shihonkin,
            nouki=nouki
        )
        supplier.save()  # 仕入先情報を保存
        messages.success(request, 'Supplier registered successfully.')  # 成功メッセージを表示
        return redirect('supplier_TBL')  # 仕入先テーブルページにリダイレクト

    return render(request, '../templates/administrar/S101/Ability_to_add_records.html')

# 仕入先テーブルを表示するビュー関数
def supplier_TBL(request):
    suppliers = Shiiregyosha.objects.all()  # 全仕入先情報を取得
    return render(request, '../templates/administrar/S102/Supplier _TBL.html', {'suppliers': suppliers})

# 住所検索を処理するビュー関数
def address_search(request):
    if request.method == 'GET':
        return render(request, '../templates/administrar/S103/Housing_search.html')  # 住所検索ページを表示

    if request.method == 'POST':
        address_search = request.POST.get('address_search', '')  # POSTデータから住所検索キーワードを取得
        if address_search:
            results = Shiiregyosha.objects.filter(shiireaddress__icontains=address_search)  # 住所キーワードで仕入先を検索
            if results.exists():
                return render(request, '../templates/administrar/S103/Housing_search.html', {'results': results})  # 検索結果を表示
            else:
                messages.error(request, '一致する仕入れ先が見つかりませんでした。')  # 一致する仕入先がない場合、エラーメッセージを表示
                return render(request, '../templates/error/error_page.html', {'error_message': '一致する仕入れ先が見つかりませんでした。'})
        else:
            messages.error(request, '住所を入力してください。')  # 住所が入力されていない場合、エラーメッセージを表示
            return render(request, '../templates/error/error_page.html', {'error_message': '住所を入力してください。'})

# パスワード変更を処理するビュー関数
def change_password(request):
    if request.method == 'POST':
        empid = request.POST['employee_id']  # POSTデータから従業員IDを取得
        current_password = request.POST['current_password']  # POSTデータから現在のパスワードを取得
        new_password = request.POST['new_password']  # POSTデータから新しいパスワードを取得
        confirm_new_password = request.POST['confirm_new_password']  # POSTデータから新しいパスワード確認を取得

        try:
            employee = Employee.objects.get(empid=empid, emppasswd=current_password)  # 従業員IDと現在のパスワードで従業員情報を取得
        except Employee.DoesNotExist:
            messages.error(request, '従業員IDまたは現在のパスワードが正しくありません。')  # 従業員情報が存在しない場合、エラーメッセージを表示
            return render(request, '../templates/error/error_page.html', {'error_message': '従業員IDまたは現在のパスワードが正しくありません。'})

        if employee.emprole == 0:
            messages.error(request, '管理者のパスワードは変更できません。')  # 管理者のパスワードは変更不可
            return render(request, '../templates/error/error_page.html', {'error_message': '管理者のパスワードは変更できません。'})

        if new_password != confirm_new_password:
            messages.error(request, '新しいパスワードが一致しません。')  # 新しいパスワードが一致しない場合、エラーメッセージを表示
            return render(request, '../templates/error/error_page.html', {'error_message': '新しいパスワードが一致しません。'})

        employee.emppasswd = new_password  # 新しいパスワードを保存
        employee.save()
        messages.success(request, 'パスワードが正常に変更されました。')  # 成功メッセージを表示
        return redirect('password_change_success')

    emprole = request.session.get('emp_role')  # セッションから従業員の役割を取得
    context = {'emprole': emprole}
    return render(request, 'administrar/E103/Employee_password_change.html', context)

# パスワード変更成功ページを表示するビュー関数
def password_change_success(request):
    return render(request, 'administrar/E103/password_change_success.html')

# 患者登録を処理するビュー関数
def patient_registration(request):
    if request.method == 'POST':
        patient_id = request.POST['patid']  # POSTデータから患者IDを取得
        last_name = request.POST['patfname']  # POSTデータから患者の姓を取得
        first_name = request.POST['patiname']  # POSTデータから患者の名を取得
        insurance_number = request.POST['hokenmei']  # POSTデータから保険番号を取得
        expiration_date = request.POST['hokenexp']  # POSTデータから保険の有効期限を取得

        if not all([patient_id, last_name, first_name, insurance_number, expiration_date]):
            messages.error(request, '全ての項目を入力してください。')  # 必要な項目が全て入力されていない場合、エラーメッセージを表示
            return render(request, '../templates/error/error_page.html', {'error_message': '全ての項目を入力してください。'})

        if Patient.objects.filter(patid=patient_id).exists():
            messages.error(request, '患者IDが既に存在します。')  # 患者IDが既に存在する場合、エラーメッセージを表示
            return render(request, '../templates/error/error_page.html', {'error_message': '患者IDが既に存在します。'})

        patient = Patient(
            patid=patient_id,
            patfname=first_name,
            patiname=last_name,
            hokenmei=insurance_number,
            hokenexp=expiration_date
        )
        patient.save()  # 患者情報を保存

        messages.success(request, '患者が正常に登録されました。')  # 成功メッセージを表示
        return redirect('patient_registration_success')

    return render(request, '../templates/reception/P101/Patient_registration.html')

# 患者登録成功ページを表示するビュー関数
def patient_registration_success(request):
    return render(request, '../templates/reception/P101/patient_registration_succes.html')

# 保険変更成功ページを表示するビュー関数
def patient_insurance_change_success(request):
    return render(request, '../templates/reception/P102/patient_insurance_change_success.html')

# 患者リストを表示するビュー関数
def patient_list(request):
    patients = Patient.objects.all()  # 全患者情報を取得
    return render(request, '../templates/reception/P102/patient_list.html', {'patients': patients})

# 患者の保険情報を編集するビュー関数
def edit_patient_insurance(request, patid):
    patient = get_object_or_404(Patient, patid=patid)  # 患者IDに対応する患者情報を取得

    if request.method == 'POST':
        insurance_number = request.POST['insurance_number']  # POSTデータから保険番号を取得
        expiration_date = request.POST['expiration_date']  # POSTデータから保険の有効期限を取得

        if insurance_number:
            patient.hokenmei = insurance_number  # 保険番号を更新

        if expiration_date:
            patient.hokenexp = expiration_date  # 保険の有効期限を更新

        patient.save()
        messages.success(request, '保険証情報が正常に変更されました。')  # 成功メッセージを表示
        return redirect('patient_list')

    return render(request, 'reception/P102/edit_patient_insurance.html', {'patient': patient})

# 患者検索を処理するビュー関数
def search_patients(request):
    patients = []
    expiration_date_str = request.GET.get('expiration_date')  # GETデータから有効期限を取得
    if expiration_date_str:
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()  # 有効期限を日付に変換
        patients = Patient.objects.filter(hokenexp__lt=expiration_date)  # 有効期限が過ぎた患者を検索
    else:
        patients = Patient.objects.all()  # 全患者情報を取得

    emprole = request.session.get('emp_role', None)  # セッションから従業員の役割を取得

    context = {
        'patients': patients,
        'emprole': emprole,
    }
    return render(request, 'reception/P104/Patient_search.html', context)

# 処置を追加するビュー関数
def add_treatment(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')  # POSTデータから患者IDを取得
        doctor_id = request.session.get('userID')  # セッションから医師IDを取得
        medicine_id = request.POST.get('medicine_id')  # POSTデータから薬剤IDを取得
        quantity = request.POST.get('quantity')  # POSTデータから数量を取得

        patient = get_object_or_404(Patient, pk=patient_id)  # 患者情報を取得
        doctor = get_object_or_404(Employee, pk=doctor_id)  # 医師情報を取得
        medicine = get_object_or_404(Medicine, pk=medicine_id)  # 薬剤情報を取得

        treatment = Treatment(patient=patient, doctor=doctor, medicine=medicine, quantity=quantity)
        treatment.save()  # 処置情報を保存

        return redirect('confirm_treatment', treatment_id=treatment.treatmentid)  # 確認画面にリダイレクト

    patients = Patient.objects.all()  # 全患者情報を取得
    medicines = Medicine.objects.all()  # 全薬剤情報を取得
    context = {
        'patients': patients,
        'medicines': medicines
    }
    return render(request, '../templates/doctor/D101/add_treatment.html', context)

# 処置追加成功ページを表示するビュー関数
def treatment_success(request):
    return render(request, '../templates/doctor/D101/treatment_success.html')

# 処置数量減少を処理するビュー関数
def decrease_treatment_quantity(request):
    if request.method == 'POST':
        treatment_id = request.POST['treatment_id']  # フォームから処置IDを取得
        decrement_value = int(request.POST['decrement_value'])  # フォームから減少する数量を取得

        treatment = get_object_or_404(Treatment, pk=treatment_id)  # 処置IDに対応する処置情報を取得

        if decrement_value > treatment.quantity:
            messages.error(request, '減少量が現在の数量を超えています。')  # 減少量が現在の数量を超えている場合、エラーメッセージを表示
            return render(request, '../templates/error/error_page.html', {
                'error_message': '減少量が現在の数量を超えています。',
                'treatments': Treatment.objects.all()
            })

        request.session['treatment_id'] = treatment_id  # セッションに処置IDを保存
        request.session['decrement_value'] = decrement_value  # セッションに減少する数量を保存

        return redirect('confirm_decrease_treatment_quantity')  # 確認画面にリダイレクト

    return render(request, 'doctor/D102/decrease_treatment_quantity.html', {
        'treatments': Treatment.objects.all()
    })

# 処置数量減少の確認と確定を処理するビュー関数
def confirm_decrease_treatment_quantity(request):
    treatment_id = request.session.get('treatment_id')  # セッションから処置IDを取得
    decrement_value = request.session.get('decrement_value')  # セッションから減少する数量を取得

    if not treatment_id or not decrement_value:
        messages.error(request, '無効なリクエストです。')  # 必要な情報がセッションにない場合、エラーメッセージを表示
        return redirect('decrease_treatment_quantity')

    treatment = get_object_or_404(Treatment, pk=treatment_id)  # 処置IDに対応する処置情報を取得

    if request.method == 'POST':
        if decrement_value > treatment.quantity:
            messages.error(request, '減少量が現在の数量を超えています。')  # 減少量が現在の数量を超えている場合、エラーメッセージを表示
            return render(request, '../templates/error/error_page.html', {
                'error_message': '減少量が現在の数量を超えています。',
                'treatment': treatment
            })

        treatment.quantity -= decrement_value  # 処置の数量を減少させる
        treatment.confirmed = True  # 確定フラグを設定
        treatment.save()  # 処置情報を保存

        if treatment.quantity == 0:
            treatment.delete()  # 処置の数量が0になった場合、処置を削除
            return redirect('treatment_deleted_success')

        messages.success(request, '処置数量が正常に減少されました。')  # 成功メッセージを表示
        return redirect('treatment_decreased_success')

    context = {
        'treatment': treatment,
        'decrement_value': decrement_value
    }
    return render(request, 'doctor/D103/confirm_treatment.html', context)

# 処置数量減少成功ページを表示するビュー関数
def treatment_decreased_success(request):
    return render(request, 'doctor/D102/treatment_decreased_success.html')

# 処置削除成功ページを表示するビュー関数
def treatment_deleted_success(request):
    return render(request, '../templates/doctor/D102/treatment_deleted.html')



def confirm_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, pk=treatment_id)  # 処置IDに対応する処置情報を取得

    if request.method == 'POST':
        treatment.confirmed = True  # 確定フラグを設定
        treatment.save()  # 処置情報を保存
        messages.success(request, '処置が正常に確定されました。')  # 成功メッセージを表示
        return redirect('treatment_success')

    context = {
        'treatment': treatment
    }
    return render(request, '../templates/doctor/D103/confirm_treatment.html', context)


# 処置の確認を行うビュー関数
def treatment_history(request):
    patient = None
    patients = None
    treatments = None

    if request.method == 'POST':
        if 'patid_search' in request.POST:
            patid = request.POST.get('patid')  # POSTデータから患者IDを取得
            if patid:
                if Patient.objects.filter(patid=patid).exists():
                    patient = get_object_or_404(Patient, patid=patid)  # 患者情報を取得
                    treatments = Treatment.objects.filter(patient=patient)  # 患者に関連する処置情報を取得
                else:
                    query_string = urlencode({'error_message': '該当する患者が見つかりません。'})
                    return HttpResponseRedirect(f"/error_page/?{query_string}")  # 該当する患者がいない場合、エラーページにリダイレクト
        elif 'all_patients' in request.POST:
            patients = Patient.objects.all()  # 全患者情報を取得
            treatments = Treatment.objects.all()  # 全処置情報を取得

    context = {
        'patient': patient,
        'patients': patients,
        'treatments': treatments,
    }

    return render(request, '../templates/doctor/D104/treatment_history.html', context)

# エラーページを表示するビュー関数
def error_page(request):
    error_message = request.GET.get('error_message', 'エラーが発生しました。')  # GETデータからエラーメッセージを取得
    emprole = request.session.get('emp_role')  # セッションから従業員の役割を取得
    return render(request, '../templates/error/error_page.html', {'error_message': error_message, 'emprole': emprole})