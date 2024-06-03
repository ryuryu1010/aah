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
    # ログアウト機能
    path('logout/', views.logout, name='logout'),
    # 従業員登録機能
    path('employee_registration/', views.employee_registration, name='employee_registration'),
    # 従業員一覧機能
    path('employee_list/', views.employee_list, name='employee_list'),
    # 仕入先追加フォーム機能
    path('Add_vendor/', views.Add_vendor, name='Add_vendor'),
    # 仕入先一覧機能
    path('supplier_TBL/', views.supplier_TBL, name='supplier_TBL'),
    # 住所検索機能
    path('address_search/', views.address_search, name='address_search'),
    # 従業員表のパスワード変更機能
    path('change_password/', views.change_password, name='change_password'),
    # 従業員（パスワード）機能
    path('password_change_success/', views.password_change_success, name='password_change_success'),
    # 患者登録機能
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    # 登録成功画面
    path('patient_registration_success/', views.patient_registration_success, name='patient_registration_success'),
    # 患者一覧
    path('patients/', views.patient_list, name='patient_list'),
    # 保険証情報編集機能
    path('edit_patient_insurance/<str:patid>/', views.edit_patient_insurance, name='edit_patient_insurance'),
    # 患者検索（保険証切れ＆全件）機能
    path('search_patients/', views.search_patients, name='search_patients'),
    # 追加
    path('add_treatment/', views.add_treatment, name='add_treatment'),
    # 処置確定
    path('confirm_treatment/<int:treatment_id>/', views.confirm_treatment, name='confirm_treatment'),
    # 処置確定成功画面
    path('treatment_success/', views.treatment_success, name='treatment_success'),
    # 処置削除と数量減少
    path('decrease_treatment_quantity/', views.decrease_treatment_quantity, name='decrease_treatment_quantity'),
    # 処置削除成功画面
    path('treatment_deleted/', views.treatment_deleted, name='treatment_deleted'),
    # 処置数量減少
    path('decrease_treatment_quantity/<int:treatment_id>/', views.decrease_treatment_quantity, name='decrease_treatment_quantity'),  # 新しいURLパターン
    # 処置履歴
    path('treatment_history/', views.treatment_history, name='treatment_history'),
    # エラーページ
    path('error_page/', views.error_page, name='error_page'),
]
