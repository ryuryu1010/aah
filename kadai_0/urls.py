from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('a_index/', views.a_index, name='a_index'),
    path('r_index/', views.r_index, name='r_index'),
    path('d_index/', views.d_index, name='d_index'),
    path('logout/', views.logout, name='logout'),
    path('employee_registration/', views.employee_registration, name='employee_registration'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('Add_vendor/', views.Add_vendor, name='Add_vendor'),
    path('supplier_TBL/', views.supplier_TBL, name='supplier_TBL'),
    path('address_search/', views.address_search, name='address_search'),
    path('change_password_0/', views.change_password_0, name='change_password_0'),
    path('password_change_success/', views.password_change_success, name='password_change_success'),
    path('change_password_1/', views.change_password_1, name='change_password_1'),
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('patient_registration_succes/', views.patient_registration_success, name='patient_registration_success'),
    path('patients/', views.patient_list, name='patient_list'),
    path('edit_patient_insurance/<str:patid>/', views.edit_patient_insurance, name='edit_patient_insurance'),
    path('insurance_expiration_check/', views.insurance_expiration_check, name='insurance_expiration_check'),


    # 他のパスの定義を追加してください
]
