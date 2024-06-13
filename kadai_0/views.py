import re  # 正規表現モジュールのインポート
from audioop import reverse  # reverse関数のインポート
from datetime import datetime, timezone  # datetimeとtimezoneモジュールのインポート

from django.http import HttpResponseRedirect  # HttpResponseRedirectをインポート
from django.shortcuts import render, redirect, get_object_or_404  # Djangoのショートカット関数をインポート
from django.contrib import messages  # Djangoのメッセージフレームワークをインポート
from django.utils.dateparse import parse_date  # 日付の解析モジュールをインポート
from django.db.models import Q  # OR条件を作成するためのモジュールをインポート
from .models import Employee, Shiiregyosha, Patient, Treatment, Medicine  # モデルをインポート
from urllib.parse import urlencode  # URLエンコードモジュールをインポート


# カスタム例外の定義
class BOException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# ログイン処理を行うビュー関数
def login(request):
    if request.method == "GET":
        # ログインページを表示するためのGETリクエスト処理
        return render(request, '../templates/login/login.html')

    if request.method == "POST":
        # POSTデータからユーザーIDとパスワードを取得
        userID = request.POST['userID']
        password = request.POST['password']
        # セッションにユーザーIDを保存
        request.session['userID'] = userID

        try:
            # ユーザーIDとパスワードで従業員情報を取得
            emp_info = Employee.objects.get(empid=userID, emppasswd=password)
            # セッションに従業員の役割を保存
            request.session['emp_role'] = emp_info.emprole

            # 役割に応じて異なるホーム画面を表示
            if emp_info.emprole == 0:
                return render(request, '../templates/index/a_index.html')
            elif emp_info.emprole == 1:
                return render(request, '../templates/index/d_index.html')
            elif emp_info.emprole == 2:
                return render(request, '../templates/index/r_index.html')

        except Employee.DoesNotExist:
            # 従業員情報が存在しない場合のエラーメッセージ表示
            return render(request, '../templates/error/login_error.html',
                          {'error_message': 'ユーザーIDまたはパスワードが間違っています'})


# 管理者ホーム画面を表示するビュー関数
def a_index(request):
    # 管理者ホーム画面を表示
    return render(request, '../templates/index/a_index.html')


# 受付ホーム画面を表示するビュー関数
def r_index(request):
    # 受付ホーム画面を表示
    return render(request, '../templates/index/r_index.html')


# 医師ホーム画面を表示するビュー関数
def d_index(request):
    # 医師ホーム画面を表示
    return render(request, '../templates/index/d_index.html')


# 仕入先TBLホーム画面を表示するビュー関数
def supplier_tbl_home(request):
    return render(request, '../templates/index/supplier_tbl_home.html')

# 他病院TBLホーム画面を表示するビュー関数
def hospital_tbl_home(request):
    return render(request, '../templates/index/hospital_tbl_home.html')


# ログアウト処理を行うビュー関数
def logout(request):
    from django.contrib.auth import logout as auth_logout
    # ログアウト処理を実行
    auth_logout(request)
    # ログアウトページを表示
    return render(request, '../templates/logout/logout.html')


# 従業員登録を処理するビュー関数
def employee_registration(request):
    if request.method == 'POST':
        # POSTデータから従業員情報を取得
        empid = request.POST['empid']
        empfname = request.POST['empfname']
        empiname = request.POST['empiname']
        emppasswd1 = request.POST['emppasswd1']
        emppasswd2 = request.POST['emppasswd2']
        emprole = request.POST['emprole']

        try:
            # パスワードの一致確認
            if emppasswd1 != emppasswd2:
                raise BOException('パスワードが一致しません。')

            # 従業員IDの重複確認
            if Employee.objects.filter(empid=empid).exists():
                raise BOException('従業員IDが既に存在します。')

            # 従業員情報の保存
            employee = Employee(
                empid=empid,
                empfname=empfname,
                empiname=empiname,
                emppasswd=emppasswd1,
                emprole=emprole
            )
            employee.save()
            messages.success(request, '従業員が正常に登録されました。')
            return redirect('employee_list')

        except BOException as e:
            # カスタム例外のメッセージを表示
            messages.error(request, str(e))
            return render(request, '../templates/error/error_page.html', {'error_message': str(e)})

    # 従業員登録ページを表示
    return render(request, '../templates/administrar/E101/Current _employee_registration_function.html')


# 従業員リストを表示するビュー関数
def employee_list(request):
    try:
        # 全従業員情報を取得
        employees = Employee.objects.all()
    except Exception:
        # エラーメッセージを表示
        return render(request, '../templates/error/error_page.html',
                      {'error_message': '従業員一覧を取得できませんでした。'})

    # 従業員リストページを表示
    return render(request, '../templates/administrar/E101/employee_list.html', {'employees': employees})


# 仕入先追加を処理するビュー関数
def Add_vendor(request):
    if request.method == 'POST':
        # POSTデータから仕入先情報を取得
        shiireid = request.POST['shiireid']
        shiiremei = request.POST['shiiremei']
        shiireaddress = request.POST['shiireaddress']
        shiiretel = request.POST['shiiretel']
        shihonkin = request.POST['shihonkin']
        nouki = request.POST['nouki']

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

        # 仕入先IDの重複確認
        if Shiiregyosha.objects.filter(shiireid=shiireid).exists():
            return redirect('/error_page/?error_message=仕入先IDが既に存在します。')

        # 仕入先情報の保存
        supplier = Shiiregyosha(
            shiireid=shiireid,
            shiiremei=shiiremei,
            shiireaddress=shiireaddress,
            shiiretel=shiiretel,
            shihonkin=shihonkin,
            nouki=nouki
        )
        supplier.save()
        messages.success(request, '仕入先が正常に登録されました。')
        return redirect('supplier_TBL')

    # 仕入先追加ページを表示
    return render(request, '../templates/administrar/S101/Ability_to_add_records.html')


# 仕入先テーブルを表示するビュー関数
def supplier_TBL(request):
    try:
        # 全仕入先情報を取得
        suppliers = Shiiregyosha.objects.all()
    except Exception:
        # エラーメッセージを表示
        return render(request, '../templates/error/error_page.html',
                      {'error_message': '仕入先一覧を取得できませんでした。'})

    # 仕入先テーブルページを表示
    return render(request, '../templates/administrar/S102/Supplier _TBL.html', {'suppliers': suppliers})


# 住所検索を処理するビュー関数
def address_search(request):
    if request.method == 'GET':
        # 住所検索ページを表示
        return render(request, '../templates/administrar/S103/Housing_search.html')

    if request.method == 'POST':
        # POSTデータから住所検索キーワードを取得
        address_search = request.POST.get('address_search', '')
        if address_search:
            # 住所キーワードで仕入先を検索
            results = Shiiregyosha.objects.filter(shiireaddress__icontains=address_search)
            if results.exists():
                # 検索結果を表示
                return render(request, '../templates/administrar/S103/Housing_search.html',
                              {'results': results})
            else:
                # 一致する仕入れ先が見つからない場合のエラーメッセージ表示
                return render(request, '../templates/error/error_page.html',
                              {'error_message': '一致する仕入れ先が見つかりませんでした。'})
        else:
            # 住所が入力されていない場合のエラーメッセージ表示
            return render(request, '../templates/error/error_page.html', {'error_message': '住所を入力してください。'})


# 資本金で仕入れ先を検索するビュー
def search_by_capital(request):
    query = request.GET.get('capital')
    suppliers = None
    if query:
        # 入力バリデーション: 全角・半角の数字、円記号、カンマ以外はエラー
        if not re.match(r'^[0-9０-９＄\$￥\\,]*$', query):
            return render(request, '../templates/error/error_page.html', {'error_message': '無効な文字が含まれています。'})

        # 半角数字に変換
        capital_str = re.sub(r'[＄\$￥\\,]', '', query)  # 円記号とカンマを削除
        capital_str = capital_str.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

        try:
            capital = int(capital_str)
            suppliers = Shiiregyosha.objects.filter(shihonkin__gte=capital)
            if not suppliers.exists():
                suppliers = None
                message = f"資本金が{capital}以上の仕入れ先は見つかりませんでした。"
            else:
                message = None
        except ValueError:
            suppliers = None
            message = "有効な数字を入力してください。"
    else:
        message = None

    return render(request, '../templates/administrar/S104/search_by_capital.html', {'suppliers': suppliers, 'query': query, 'message': message})


# 仕入先一覧表示ビュー
def supplier_list(request):
    query = request.GET.get('q')
    if query:
        suppliers = Shiiregyosha.objects.filter(shiiremei__icontains=query)
    else:
        suppliers = Shiiregyosha.objects.all()
    return render(request, '../templates/administrar/S105/supplier_list.html', {'suppliers': suppliers})



# 電話番号変更ビュー
def change_phone_number(request, shiireid):
    # 仕入れ先オブジェクトを取得、存在しない場合は404エラー
    supplier = get_object_or_404(Shiiregyosha, pk=shiireid)

    if request.method == 'POST':
        new_telephone = request.POST.get('new_telephone')  # 新しい電話番号を取得
        error_message = None

        # 電話番号が数字、括弧、ハイフンのみを含むかどうかをチェック
        if not re.match(r'^[0-9()-]+$', new_telephone):
            error_message = "電話番号は半角数字、括弧、ハイフンのみを含むことができます。"
        # 電話番号の長さをチェック（11桁から15桁）
        elif len(new_telephone) < 11 or len(new_telephone) > 15:
            error_message = "電話番号は11桁から15桁でなければなりません。"
        # 新しい電話番号が現在の電話番号と同じかどうかをチェック
        elif new_telephone == supplier.shiiretel:
            error_message = "新しい電話番号が現在の電話番号と同じです。"

        if error_message:
            # エラーがある場合はエラーページを表示
            return render(request, '../templates/error/error_page.html', {'error_message': error_message})
        else:
            # 電話番号を更新して保存
            supplier.shiiretel = new_telephone
            supplier.save()
            # 成功画面を表示
            return render(request, '../templates/administrar/S105/phone_change_success.html', {'supplier': supplier})

    # GETリクエストの場合、変更ページを表示
    return render(request, '../templates/administrar/S105/change_phone_number.html', {'supplier': supplier})



# パスワード変更を処理するビュー関数
def change_password(request):
    # セッションから従業員の役割を取得
    emprole = request.session.get('emp_role')
    if request.method == 'POST':
        # 管理者の場合、POSTデータから従業員IDを取得
        if emprole == 0:
            empid = request.POST['employee_id']
        else:
            # 受付の場合、セッションから従業員IDを取得
            empid = request.session.get('userID')

        # POSTデータから現在のパスワードと新しいパスワードを取得
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        try:
            # 従業員IDと現在のパスワードで従業員情報を取得
            employee = Employee.objects.get(empid=empid, emppasswd=current_password)
        except Employee.DoesNotExist:
            # 従業員情報が存在しない場合のエラーメッセージ表示
            return render(request, '../templates/error/error_page.html',
                          {'error_message': '従業員IDまたは現在のパスワードが正しくありません。'})

        # 新しいパスワードの一致確認
        if new_password != confirm_new_password:
            # 新しいパスワードが一致しない場合のエラーメッセージ表示
            return render(request, '../templates/error/error_page.html',
                          {'error_message': '新しいパスワードが一致しません。'})

        # 新しいパスワードを保存
        employee.emppasswd = new_password
        employee.save()
        messages.success(request, 'パスワードが正常に変更されました。')
        return redirect('password_change_success')

    # 管理者の場合、他の管理者を除外して全従業員情報を取得し、管理者自身の情報も取得
    employees = Employee.objects.exclude(emprole=0) if emprole == 0 else None
    if emprole == 0:
        # 管理者自身の情報をセッションに保存
        admin = Employee.objects.get(empid=request.session.get('userID'))
        request.session['current_password'] = admin.emppasswd

    context = {'employees': employees, 'emprole': emprole}
    # パスワード変更ページを表示
    return render(request, 'administrar/E103/Employee_password_change.html', context)



# パスワード変更成功ページを表示するビュー関数
def password_change_success(request):
    # パスワード変更成功ページを表示
    return render(request, 'administrar/E103/password_change_success.html')


# 更新成功のビュー関数
def employee_update_success(request):
    return render(request, '../templates/administrar/E102/employee_update_success.html')


# 従業員情報更新のビュー関数
def employee_update(request):
    employees = Employee.objects.all()  # すべての従業員を取得
    employee = None

    if request.method == "POST":
        empid = request.POST.get('empid')
        new_empfname = request.POST.get('new_empfname')
        new_empiname = request.POST.get('new_empiname')

        if not empid or not new_empfname or not new_empiname:
            # すべてのフィールドが入力されていない場合
            return render(request, '../templates/error/error_page.html',
                          {'error_message': 'すべてのフィールドを入力してください。', 'emprole': request.user.emprole})
        else:
            try:
                employee = Employee.objects.get(empid=empid)
                # 氏名が変更されていない場合
                if employee.empfname == new_empfname and employee.empiname == new_empiname:
                    return render(request, '../templates/error/error_page.html',
                                  {'error_message': '氏名が変更されていません。', 'emprole': request.user.emprole})
                # 氏名を更新
                employee.empfname = new_empfname
                employee.empiname = new_empiname
                employee.save()  # データベースに保存
                return redirect('employee_update_success')  # 更新成功後に成功画面にリダイレクト
            except Employee.DoesNotExist:
                # 従業員IDが見つからない場合
                return render(request, '../templates/error/error_page.html',
                              {'error_message': '従業員IDが見つかりません。', 'emprole': request.user.emprole})

    return render(request, '../templates/administrar/E102/employee_update.html', {'employees': employees, 'employee': employee})


# 患者登録を処理するビュー関数
def patient_registration(request):
    if request.method == 'POST':
        # POSTデータから患者情報を取得
        patient_id = request.POST['patid']
        last_name = request.POST['patfname']
        first_name = request.POST['patiname']
        insurance_number = request.POST['hokenmei']
        expiration_date = request.POST['hokenexp']

        # 全ての項目が入力されていることを確認
        if not all([patient_id, last_name, first_name, insurance_number, expiration_date]):
            # 入力漏れがある場合のエラーメッセージ表示
            return render(request, '../templates/error/error_page.html',
                          {'error_message': '全ての項目を入力してください。'})

        # 患者IDの重複確認
        if Patient.objects.filter(patid=patient_id).exists():
            return render(request, '../templates/error/error_page.html', {'error_message': '患者IDが既に存在します。'})

        # 患者情報の保存
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

    # 患者登録ページを表示
    return render(request, '../templates/reception/P101/Patient_registration.html')


# 患者登録成功ページを表示するビュー関数
def patient_registration_success(request):
    # 患者登録成功ページを表示
    return render(request, '../templates/reception/P101/patient_registration_success.html')


# 保険変更成功ページを表示するビュー関数
def patient_insurance_change_success(request):
    # 保険変更成功ページを表示
    return render(request, '../templates/reception/P102/patient_insurance_change_success.html')


# 患者リストを表示するビュー関数
def patient_list(request):
    try:
        # 全患者情報を取得
        patients = Patient.objects.all()
    except Exception:
        # エラーメッセージを表示
        return render(request, '../templates/error/error_page.html',
                      {'error_message': '患者リストを取得できませんでした。'})

    # 患者リストページを表示
    return render(request, '../templates/reception/P102/patient_list.html', {'patients': patients})


# 患者の保険情報を編集するビュー関数
def edit_patient_insurance(request, patid):
    # 患者IDに対応する患者情報を取得
    patient = get_object_or_404(Patient, patid=patid)

    if request.method == 'POST':
        # POSTデータから保険証記号番号と有効期限を取得
        hokenmei = request.POST['hokenmei']
        expiration_date_str = request.POST['expiration_date']
        expiration_date = parse_date(expiration_date_str)

        # 保険証番号が10桁であることを確認
        if len(hokenmei) != 10:
            error_message = '保険証番号は10桁でなければなりません。'
            return render(request, '../templates/error/error_page.html', {'error_message': error_message})

        if expiration_date:
            # 新しい有効期限が現在の有効期限より後の日付であることを確認
            if expiration_date <= patient.hokenexp:
                error_message = '新しい有効期限は現在の有効期限より後の日付にしてください。'
                return render(request, '../templates/error/error_page.html', {'error_message': error_message})

            # 保険の有効期限を更新
            patient.hokenexp = expiration_date

        # 保険証記号番号を更新
        patient.hokenmei = hokenmei
        patient.save()

        return redirect('insurance_change_success')

    # 保険情報編集ページを表示
    return render(request, 'reception/P102/edit_patient_insurance.html', {'patient': patient})


# 保険変更成功ページを表示するビュー関数
def insurance_change_success(request):
    # 保険変更成功ページを表示
    return render(request, 'reception/P102/patient_insurance_change_success.html')


# 患者検索を処理するビュー関数
def search_patients(request):
    # 検索結果の患者リストを初期化
    patients = []
    # セッションから従業員の役割を取得
    emprole = request.session.get('emp_role', None)
    # エラーメッセージを初期化
    error_message = None

    if request.method == 'POST':
        # 受付用の検索処理 (emprole == 2)
        if emprole == 2:
            expiration_date_str = request.POST.get('expiration_date')
            patfname = request.POST.get('patfname')
            patiname = request.POST.get('patiname')

            if expiration_date_str or patfname or patiname:
                try:
                    # 患者をフィルタリングするクエリセットを取得
                    patients = Patient.objects.all()

                    if expiration_date_str:
                        # 有効期限を日付に変換
                        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
                        # 有効期限が過ぎた患者をフィルタリング
                        patients = patients.filter(hokenexp__lt=expiration_date)

                    if patfname:
                        # 部分一致で姓をフィルタリング
                        patients = patients.filter(patfname__icontains=patfname)

                    if patiname:
                        # 部分一致で名をフィルタリング
                        patients = patients.filter(patiname__icontains=patiname)

                    if not patients.exists():
                        error_message = '該当する患者が見つかりません。'
                except ValueError:
                    # 有効期限の変換に失敗した場合のエラーハンドリング
                    error_message = '有効な日付を入力してください。'
            else:
                # 検索条件が入力されていない場合のエラーメッセージ
                error_message = '検索条件を入力してください。'

        # 医師用の検索処理 (emprole == 1)
        elif emprole == 1:
            patfname = request.POST.get('patfname')
            patiname = request.POST.get('patiname')
            if patfname or patiname:
                # すべての患者を取得
                patients = Patient.objects.all()
                if patfname:
                    # 部分一致で姓をフィルタリング
                    patients = patients.filter(patfname__icontains=patfname)
                if patiname:
                    # 部分一致で名をフィルタリング
                    patients = patients.filter(patiname__icontains=patiname)
                if not patients.exists():
                    # 該当する患者が見つからなかった場合のエラーハンドリング
                    error_message = '該当する患者が見つかりません。'
            else:
                # 姓または名が入力されていない場合のエラーハンドリング
                error_message = '検索条件を入力してください。'

    context = {
        'patients': patients,
        'emprole': emprole,
        'error_message': error_message,
    }
    # 検索結果をテンプレートにレンダリングして表示
    return render(request, 'reception/P104/Patient_search.html', context)



# 処置を追加するビュー関数
def add_treatments(request):
    # 全患者情報を取得
    patients = Patient.objects.all()
    # 全薬剤情報を取得
    medicines = Medicine.objects.all()

    if request.method == 'POST':
        treatment_data = []
        for key in request.POST.keys():
            if key.startswith('patient_id_'):
                index = key.split('_')[-1]
                # POSTデータから処置情報を取得
                patient_id = request.POST.get(f'patient_id_{index}')
                medicine_id = request.POST.get(f'medicine_id_{index}')
                quantity = request.POST.get(f'quantity_{index}')
                if patient_id and medicine_id and quantity:
                    # 数量が正の整数であることを確認
                    if int(quantity) <= 0:
                        messages.error(request, '数量は正の整数でなければなりません。')
                        return redirect('add_treatments')
                    treatment_data.append({
                        'patient_id': patient_id,
                        'medicine_id': medicine_id,
                        'quantity': quantity,
                    })

        # 処置データをセッションに保存して確認画面に渡す
        request.session['treatment_data'] = treatment_data
        return redirect('confirm_treatments')

    context = {
        'patients': patients,
        'medicines': medicines,
    }
    # 処置追加ページを表示
    return render(request, '../templates/doctor/D101/add_treatment.html', context)


# 処置確定を行うビュー関数
def confirm_treatments(request):
    # セッションから処置データを取得
    treatment_data = request.session.get('treatment_data', [])
    # セッションから医師IDを取得
    doctor_id = request.session.get('userID')

    if request.method == 'POST':
        for data in treatment_data:
            patient = get_object_or_404(Patient, pk=data['patient_id'])
            doctor = get_object_or_404(Employee, pk=doctor_id)
            medicine = get_object_or_404(Medicine, pk=data['medicine_id'])
            quantity = int(data['quantity'])
            if quantity <= 0:
                messages.error(request, '数量は正の整数でなければなりません。')
                return redirect('add_treatments')

            # 処置情報の保存
            treatment = Treatment(patient=patient, doctor=doctor, medicine=medicine, quantity=quantity)
            treatment.save()

        messages.success(request, '処置が正常に追加されました。')
        return redirect('treatment_success')

    treatments = []
    for data in treatment_data:
        patient = get_object_or_404(Patient, pk=data['patient_id'])
        medicine = get_object_or_404(Medicine, pk=data['medicine_id'])
        treatments.append({
            'patient': patient,
            'medicine': medicine,
            'quantity': data['quantity']
        })

    context = {
        'treatment_data': treatments,
    }
    # 処置確認ページを表示
    return render(request, '../templates/doctor/D103/confirm_treatment.html', context)


# 処置追加成功ページを表示するビュー関数
def treatment_success(request):
    # 処置追加成功ページを表示
    return render(request, '../templates/doctor/D103/treatment_success.html')



# 処置の確認を行うビュー関数
def treatment_history(request):
    patient = None
    patients = None
    treatments = None

    if request.method == 'POST':
        if 'patid_search' in request.POST:
            patid = request.POST.get('patid')
            if patid:
                if Patient.objects.filter(patid=patid).exists():
                    # 患者情報を取得
                    patient = get_object_or_404(Patient, patid=patid)
                    # 患者に関連する処置情報を取得
                    treatments = Treatment.objects.filter(patient=patient)
                else:
                    # 該当する患者が見つからない場合のエラーメッセージ表示
                    return render(request, '../templates/error/error_page.html',
                                  {'error_message': '該当する患者が見つかりません。'})
        elif 'all_patients' in request.POST:
            # 全患者情報を取得
            patients = Patient.objects.all()
            # 全処置情報を取得
            treatments = Treatment.objects.all()

    context = {
        'patient': patient,
        'patients': patients,
        'treatments': treatments,
    }
    # 処置履歴ページを表示
    return render(request, '../templates/doctor/D104/treatment_history.html', context)


# エラーページを表示するビュー関数
def error_page(request):
    # GETデータからエラーメッセージを取得
    error_message = request.GET.get('error_message', 'エラーが発生しました。')
    # セッションから従業員の役割を取得
    emprole = request.session.get('emp_role', None)
    # エラーページを表示
    return render(request, '../templates/error/error_page.html', {'error_message': error_message, 'emprole': emprole})




















# 処置数量を複数一度に減らすためのビュー関数
def reduce_multiple_treatment_quantities(request):
    # すべての処置情報を取得
    treatments = Treatment.objects.all()
    # GETデータから検索クエリを取得
    search_query = request.GET.get('search', '')

    if search_query:
        # 検索クエリがある場合、患者の姓または名でフィルタリング
        treatments = treatments.filter(
            Q(patient__patfname__icontains=search_query) |
            Q(patient__patiname__icontains=search_query)
        )

    if request.method == 'POST':
        # POSTデータから処置IDのリストを取得
        treatment_ids = request.POST.getlist('treatment_ids')
        # POSTデータから減少量を取得
        quantity_reduction = int(request.POST['quantity_reduction'])
        try:
            # 処置が選択されていない場合のエラーメッセージ表示
            if not treatment_ids:
                raise BOException('処置が選択されていません。')

            # 減少量が正の整数でない場合のエラーメッセージ表示
            if quantity_reduction <= 0:
                raise BOException('減少量は正の整数でなければなりません。')

            # 処置IDのリストで処置情報を取得
            treatments_to_reduce = Treatment.objects.filter(treatmentid__in=treatment_ids)
            for treatment in treatments_to_reduce:
                # 処置数量が不十分な場合のエラーメッセージ表示
                if treatment.quantity - quantity_reduction < 0:
                    raise BOException(f'処置ID {treatment.treatmentid} の数量が不十分です。')

            # 処置の減少量をセッションに保存して確認画面に渡す
            request.session['treatment_ids'] = treatment_ids
            request.session['quantity_reduction'] = quantity_reduction
            return render(request, '../templates/doctor/D103/confirm_reduction.html', {'treatments': treatments_to_reduce, 'quantity_reduction': quantity_reduction})

        except BOException as e:
            # カスタム例外のメッセージを表示
            messages.error(request, str(e))
            return render(request, '../templates/error/error_page.html', {'error_message': str(e)})

    context = {
        'treatments': treatments,
    }
    # 処置数量減少画面を表示
    return render(request, '../templates/doctor/D102/reduce_multiple_treatment_quantities.html', context)


# 処置数量減少を確定するためのビュー関数
def confirm_reduction(request):
    if request.method == 'POST':
        # セッションから処置IDリストと減少量を取得
        treatment_ids = request.session.get('treatment_ids', [])
        quantity_reduction = request.session.get('quantity_reduction', 0)

        # 無効な操作に対するエラーメッセージを表示
        if not treatment_ids or quantity_reduction <= 0:
            messages.error(request, '無効な操作です。')
            return redirect('reduce_multiple_treatment_quantities')

        try:
            # 処置IDのリストで処置情報を取得
            treatments = Treatment.objects.filter(treatmentid__in=treatment_ids)
            for treatment in treatments:
                # 処置の数量を減少
                treatment.quantity -= quantity_reduction

                # 処置の数量が0以下になった場合に削除
                if treatment.quantity <= 0:
                    treatment.delete()
                else:
                    treatment.save()

            messages.success(request, '処置数量が正常に減少されました。')
            return redirect('treatment_quantity_reduction_success')

        except Exception as e:
            # エラーメッセージを表示
            messages.error(request, str(e))
            return render(request, '../templates/error/error_page.html', {'error_message': str(e)})

    # GETリクエストの場合、処置数量減少画面にリダイレクト
    return redirect('reduce_multiple_treatment_quantities')


# 処置数量減少成功ページを表示するビュー関数
def treatment_quantity_reduction_success(request):
    # 処置数量減少成功ページを表示
    return render(request, '../templates/doctor/D103/treatment_quantity_reduction_success.html')

