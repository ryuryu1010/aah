from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('employee_registration/', views.employee_registration, name='employee_registration'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('Add_vendor/', views.Add_vendor, name='Add_vendor'),
    path('supplier_TBL/', views.supplier_TBL, name='supplier_TBL'),
    path('address_search/', views.address_search, name='address_search'),
    path('change_password_0/', views.change_password_0, name='change_password_0'),
    path('password_change_success/', views.password_change_success, name='password_change_success'),
    path('change_password_1/', views.change_password_1, name='change_password_1'),
    # 他のパスの定義を追加してください
]
