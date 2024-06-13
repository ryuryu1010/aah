from django.urls import path
from . import views

urlpatterns = [
    # ログイン機能
    path('', views.login, name='login'),
    # 管理者ホーム画面
    path('a_index/', views.a_index, name='a_index'),
    # 受付ホーム画面
    path('r_index/', views.r_index, name='r_index'),
    # 医師ホーム画面
    path('d_index/', views.d_index, name='d_index'),
    # 仕入先TBLホーム画面のURLパターン
    path('supplier_tbl_home/', views.supplier_tbl_home, name='supplier_tbl_home'),
    # 他病院TBLホーム画面のURLパターン
    path('hospital_tbl_home/', views.hospital_tbl_home, name='hospital_tbl_home'),
    # ログアウト機能
    path('logout/', views.logout, name='logout'),
    # 従業員登録機能
    path('employee_registration/', views.employee_registration, name='employee_registration'),
    # 従業員一覧機能
    path('employee_list/', views.employee_list, name='employee_list'),
    # 仕入先TBL：仕入先追加フォーム機能
    path('Add_vendor/', views.Add_vendor, name='Add_vendor'),
    # 仕入先TBL：仕入先一覧機能
    path('supplier_TBL/', views.supplier_TBL, name='supplier_TBL'),
    # 仕入先TBL：住所検索機能
    path('address_search/', views.address_search, name='address_search'),
    # 仕入先TBL：資本金検索
    path('search_by_capital/', views.search_by_capital, name='search_by_capital'),
    # 仕入先TBL：仕入先一覧ページのURLパターン（電話番号変更用）
    path('supplier_list/', views.supplier_list, name='supplier_list'),
    # 仕入先TBL：電話番号変更ページのURLパターン
    path('supplier/<str:shiireid>/change_phone/', views.change_phone_number, name='change_phone_number'),
    # 他病院登録機能のURLパターン。ビュー関数register_hospitalを呼び出します。
    path('register_hospital/', views.register_hospital, name='register_hospital'),
    # 他病院一覧表示機能のURLパターン。ビュー関数hospital_listを呼び出します。
    path('hospital_list/', views.hospital_list, name='hospital_list'),
    # 住所による他病院検索機能のURLパターン。ビュー関数search_hospital_by_addressを呼び出します。
    path('search_hospital_by_address/', views.search_hospital_by_address, name='search_hospital_by_address'),
    # 資本金による他病院検索機能のURLパターン。ビュー関数search_hospital_by_capitalを呼び出します。
    path('search_hospital_by_capital/', views.search_hospital_by_capital, name='search_hospital_by_capital'),
    # 他病院情報変更機能のURLパターン。ビュー関数edit_hospital_infoを呼び出します。
    path('edit_hospital_info/<str:tabyouinid>/', views.edit_hospital_info, name='edit_hospital_info'),
    # 従業員＆管理者のパスワード変更機能
    path('change_password/', views.change_password, name='change_password'),
    # パスワード変更成功機能
    path('password_change_success/', views.password_change_success, name='password_change_success'),
    # 従業員の名前変更機能
    path('employee/update/', views.employee_update, name='employee_update'),
    # 成功画面用のURLパターン
    path('employee/update/success/', views.employee_update_success, name='employee_update_success'),
    # 患者登録機能
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    # 登録成功画面
    path('patient_registration_success/', views.patient_registration_success, name='patient_registration_success'),
    # 患者一覧
    path('patients/', views.patient_list, name='patient_list'),
    # 保険証情報編集機能
    path('edit_patient_insurance/<str:patid>/', views.edit_patient_insurance, name='edit_patient_insurance'),
    # 保険証情報編集成功
    path('insurance_change_success/', views.insurance_change_success, name='insurance_change_success'),
    # 患者検索（保険証切れ＆全件）機能
    path('search_patients/', views.search_patients, name='search_patients'),
    # 処置追加
    path('add_treatments/', views.add_treatments, name='add_treatments'),
    # 処置確認
    path('confirm_treatments/', views.confirm_treatments, name='confirm_treatments'),
    # 処置確定成功画面
    path('treatment_success/', views.treatment_success, name='treatment_success'),
    # 処置履歴
    path('treatment_history/', views.treatment_history, name='treatment_history'),
    # 処置数量減少
    path('reduce_multiple_treatment_quantities/', views.reduce_multiple_treatment_quantities, name='reduce_multiple_treatment_quantities'),
    # 処置数量減少確認
    path('confirm_reduction/', views.confirm_reduction, name='confirm_reduction'),
    # 処置数量減少成功画面
    path('treatment_quantity_reduction_success/', views.treatment_quantity_reduction_success, name='treatment_quantity_reduction_success'),
    # エラーページ
    path('error_page/', views.error_page, name='error_page'),
]
