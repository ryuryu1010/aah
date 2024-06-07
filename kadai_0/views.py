import re  # 正規表現モジュールのインポート
from audioop import reverse
from datetime import datetime, timezone

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_date

from .models import Employee, Shiiregyosha, Patient, Treatment, Medicine
from urllib.parse import urlencode


# カスタム例外の定義
class BOException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


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
            return render(request, '../templates/error/error_page.html',
                          {'error_message': 'ユーザーIDまたはパスワードが間違っています'})  # エラーページを表示


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

        try:
            if emppasswd1 != emppasswd2:
                raise BOException('パスワードが一致しません。')  # カスタム例外をスロー

            if Employee.objects.filter(empid=empid).exists():
                raise BOException('従業員IDが既に存在します。')  # カスタム例外をスロー

            employee = Employee(
                empid=empid,
                empfname=empfname,
                empiname=empiname,
                emppasswd=emppasswd1,  # パスワードをそのまま保存
                emprole=emprole
            )
            employee.save()  # 従業員情報を保存
            messages.success(request, '従業員が正常に登録されました。')  # 成功メッセージを表示
            return redirect('employee_list')  # 従業員リストページにリダイレクト

        except BOException as e:
            messages.error(request, str(e))  # カスタム例外のメッセージを表示
            return render(request, '../templates/error/error_page.html', {'error_message': str(e)})

    return render(request, '../templates/administrar/E101/Current _employee_registration_function.html')


# 従業員リストを表示するビュー関数
def employee_list(request):
    try:
        employees = Employee.objects.all()  # 全従業員情報を取得
    except Exception:
        return render(request, '../templates/error/error_page.html',
                      {'error_message': '従業員一覧を取得できませんでした。'})

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

        # フィールドの長さのバリデーション
        if len(shiireid) > 8:
            return redirect('/error_page/?error_message=仕入先IDが長すぎます。')
        if len(shiiremei) > 64:
            return redirect('/error_page/?error_message=仕入先名が長すぎます。')
        if len(shiireaddress) > 64:
            return redirect('/error_page/?error_message=仕入先住所が長すぎます。')
        if len(shiiretel) > 15:
            return redirect('/error_page/?error_message=仕入先電話番号が長すぎます。')
        if len(shiiretel) < 10:
            return redirect('/error_page/?error_message=仕入先電話番号は最低11文字である必要があります。')

        # 電話番号のバリデーション
        if not re.match(r'^[0-9()\-]+$', shiiretel):
            return redirect('/error_page/?error_message=電話番号には数字、括弧、ハイフン以外の文字は使用できません。')

        # 資本金のバリデーション
        if not re.match(r'^[0-9,¥]+$', shihonkin):
            return redirect('/error_page/?error_message=資本金には数値、カンマ、円記号以外の文字は使用できません。')

        # 納期のバリデーション
        if not re.match(r'^[0-9,]+$', nouki):
            return redirect('/error_page/?error_message=納期には数値、カンマ、以外の文字は使用できません。')

        if Shiiregyosha.objects.filter(shiireid=shiireid).exists():
            return redirect('/error_page/?error_message=仕入先IDが既に存在します。')  # 仕入先IDが既に存在する場合、エラーメッセージを表示

        supplier = Shiiregyosha(
            shiireid=shiireid,
            shiiremei=shiiremei,
            shiireaddress=shiireaddress,
            shiiretel=shiiretel,
            shihonkin=shihonkin,
            nouki=nouki
        )
        supplier.save()  # 仕入先情報を保存
        messages.success(request, '仕入先が正常に登録されました。')  # 成功メッセージを表示
        return redirect('supplier_TBL')  # 仕入先テーブルページにリダイレクト

    return render(request, '../templates/administrar/S101/Ability_to_add_records.html')


# 仕入先テーブルを表示するビュー関数
def supplier_TBL(request):
    try:
        suppliers = Shiiregyosha.objects.all()  # 全仕入先情報を取得
    except Exception:
        return render(request, '../templates/error/error_page.html',
                      {'error_message': '仕入先一覧を取得できませんでした。'})

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
                return render(request, '../templates/administrar/S103/Housing_search.html',
                              {'results': results})  # 検索結果を表示
            else:
                return render(request, '../templates/error/error_page.html',
                              {'error_message': '一致する仕入れ先が見つかりませんでした。'})
        else:
            return render(request, '../templates/error/error_page.html', {'error_message': '住所を入力してください。'})


# パスワード変更を処理するビュー関数
def change_password(request):
    emprole = request.session.get('emp_role')
    if request.method == 'POST':
        if emprole == 0:
            empid = request.POST['employee_id']  # POSTデータから従業員IDを取得（管理者の場合）
        else:
            empid = request.session.get('userID')  # セッションから従業員IDを取得（受付の場合）

        current_password = request.POST['current_password']  # POSTデータから現在のパスワードを取得
        new_password = request.POST['new_password']  # POSTデータから新しいパスワードを取得
        confirm_new_password = request.POST['confirm_new_password']  # POSTデータから新しいパスワード確認を取得

        try:
            employee = Employee.objects.get(empid=empid, emppasswd=current_password)  # 従業員IDと現在のパスワードで従業員情報を取得
        except Employee.DoesNotExist:
            return render(request, '../templates/error/error_page.html',
                          {'error_message': '従業員IDまたは現在のパスワードが正しくありません。'})

        if new_password != confirm_new_password:
            return render(request, '../templates/error/error_page.html',
                          {'error_message': '新しいパスワードが一致しません。'})

        employee.emppasswd = new_password  # 新しいパスワードを保存
        employee.save()
        messages.success(request, 'パスワードが正常に変更されました。')  # 成功メッセージを表示
        return redirect('password_change_success')

    employees = Employee.objects.exclude(emprole=0) if emprole == 0 else None  # 管理者の場合、他の管理者を除外して全従業員情報を取得
    context = {'employees': employees, 'emprole': emprole}
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
            return render(request, '../templates/error/error_page.html',
                          {'error_message': '全ての項目を入力してください。'})

        if Patient.objects.filter(patid=patient_id).exists():
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
    try:
        patients = Patient.objects.all()  # 全患者情報を取得
    except Exception:
        return render(request, '../templates/error/error_page.html',
                      {'error_message': '患者リストを取得できませんでした。'})

    return render(request, '../templates/reception/P102/patient_list.html', {'patients': patients})


# 患者の保険情報を編集するビュー関数
def edit_patient_insurance(request, patid):
    patient = get_object_or_404(Patient, patid=patid)  # 患者IDに対応する患者情報を取得

    if request.method == 'POST':
        expiration_date_str = request.POST['expiration_date']  # POSTデータから保険の有効期限を取得
        expiration_date = parse_date(expiration_date_str)  # 有効期限を日付オブジェクトに変換

        if expiration_date:
            if expiration_date <= patient.hokenexp:
                error_message = '新しい有効期限は現在の有効期限より後の日付にしてください。'
                return render(request, '../templates/error/error_page.html', {'error_message': error_message})

            patient.hokenexp = expiration_date  # 保険の有効期限を更新

        patient.save()
        return redirect('insurance_change_success')  # 成功ページにリダイレクト

    return render(request, 'reception/P102/edit_patient_insurance.html', {'patient': patient})


# 保険変更成功ページを表示するビュー関数
def insurance_change_success(request):
    return render(request, 'reception/P102/patient_insurance_change_success.html')


# 患者検索を処理するビュー関数
def search_patients(request):
    patients = []  # 検索結果の患者リストを初期化
    emprole = request.session.get('emp_role', None)  # セッションから従業員の役割を取得
    error_message = None  # エラーメッセージを初期化

    if request.method == 'POST':
        # 受付用の検索処理 (emprole == 2)
        if emprole == 2:
            expiration_date_str = request.POST.get('expiration_date')  # POSTデータから有効期限を取得
            if expiration_date_str:
                try:
                    expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()  # 有効期限を日付に変換
                    patients = Patient.objects.filter(hokenexp__lt=expiration_date)  # 有効期限が過ぎた患者を検索
                    if not patients:
                        error_message = '該当する患者が見つかりません。'
                except ValueError:
                    # 有効期限の変換に失敗した場合のエラーハンドリング
                    error_message = '有効な日付を入力してください。'
            else:
                # 有効期限が入力されていない場合のエラーハンドリング
                error_message = '有効期限を指定してください。'

        # 医師用の検索処理 (emprole == 1)
        elif emprole == 1:
            patfname = request.POST.get('patfname')  # POSTデータから患者の姓を取得
            patiname = request.POST.get('patiname')  # POSTデータから患者の名を取得
            if patfname or patiname:
                patients = Patient.objects.all()  # すべての患者を取得
                if patfname:
                    patients = patients.filter(patfname__icontains=patfname)  # 部分一致で姓をフィルタ
                if patiname:
                    patients = patients.filter(patiname__icontains=patiname)  # 部分一致で名をフィルタ
                if not patients:
                    # 該当する患者が見つからなかった場合のエラーハンドリング
                    error_message = '該当する患者が見つかりません。'
            else:
                # 姓または名が入力されていない場合のエラーハンドリング
                error_message = '検索条件を入力してください。'

    # 検索結果と役割をコンテキストに追加
    context = {
        'patients': patients,
        'emprole': emprole,
        'error_message': error_message,
    }
    # 検索結果をテンプレートにレンダリングして表示
    return render(request, 'reception/P104/Patient_search.html', context)


# 処置を追加するビュー関数
def add_treatment(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')  # POSTデータから患者IDを取得
        doctor_id = request.session.get('userID')  # セッションから医師IDを取得
        medicine_id = request.POST.get('medicine_id')  # POSTデータから薬剤IDを取得
        quantity = request.POST.get('quantity')  # POSTデータから数量を取得

        if int(quantity) <= 0:
            return render(request, '../templates/error/error_page.html',
                          {'error_message': '数量は正の整数でなければなりません。'})

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

# 処置確定を行うビュー関数
def confirm_treatment(request, treatment_id):
    treatment = get_object_or_404(Treatment, pk=treatment_id)  # 処置IDに対応する処置情報を取得

    if request.method == 'POST':
        # 処置を確定するためのロジック
        treatment.confirmed = True  # 確定フラグを設定
        treatment.save()  # 処置情報を保存

        messages.success(request, '処置が正常に確定されました。')  # 成功メッセージを表示
        return redirect('treatment_success')  # 処置成功ページにリダイレクト

    context = {
        'treatment': treatment
    }
    return render(request, '../templates/doctor/D103/confirm_treatment.html', context)


# 処置追加成功ページを表示するビュー関数
def treatment_success(request):
    return render(request, '../templates/doctor/D101/treatment_success.html')


# 処置数量減少を処理するビュー関数
def decrease_treatment_quantity(request):
    if request.method == 'POST':
        treatment_id = request.POST['treatment_id']  # フォームから処置IDを取得
        decrement_value = int(request.POST['decrement_value'])  # フォームから減少する数量を取得

        if decrement_value <= 0:
            return render(request, '../templates/error/error_page.html',
                          {'error_message': '減少量は正の整数でなければなりません。'})

        treatment = get_object_or_404(Treatment, pk=treatment_id)  # 処置IDに対応する処置情報を取得

        if decrement_value > treatment.quantity:
            return render(request, '../templates/error/error_page.html',
                          {'error_message': '減少量が現在の数量を超えています。'})

        request.session['treatment_id'] = treatment_id  # セッションに処置IDを保存
        request.session['decrement_value'] = decrement_value  # セッションに減少する数量を保存

        return redirect('confirm_decrease_treatment_quantity')  # 確認画面にリダイレクト

    return render(request, '../templates/doctor/D102/decrease_treatment_quantity.html', {
        'treatments': Treatment.objects.all()
    })


# 処置数量減少の確認と確定を処理するビュー関数
def confirm_decrease_treatment_quantity(request):
    treatment_id = request.session.get('treatment_id')  # セッションから処置IDを取得
    decrement_value = request.session.get('decrement_value')  # セッションから減少する数量を取得

    if not treatment_id or not decrement_value:
        return render(request, '../templates/error/error_page.html', {'error_message': '無効なリクエストです。'})

    treatment = get_object_or_404(Treatment, pk=treatment_id)  # 処置IDに対応する処置情報を取得

    if request.method == 'POST':
        if decrement_value > treatment.quantity:
            return render(request, '../templates/error/error_page.html',
                          {'error_message': '減少量が現在の数量を超えています。'})

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
    return render(request, '../templates/doctor/D103/confirm_treatment.html', context)


# 処置数量減少成功ページを表示するビュー関数
def treatment_decreased_success(request):
    return render(request, 'doctor/D102/treatment_decreased_success.html')


# 処置削除成功ページを表示するビュー関数
def treatment_deleted_success(request):
    return render(request, '../templates/doctor/D102/treatment_deleted.html')


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
                    return render(request, '../templates/error/error_page.html',
                                  {'error_message': '該当する患者が見つかりません。'})
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
    emprole = request.session.get('emp_role', None)  # セッションから従業員の役割を取得
    return render(request, '../templates/error/error_page.html', {'error_message': error_message, 'emprole': emprole})



