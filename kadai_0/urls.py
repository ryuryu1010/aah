from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('employee_registration/', views.employee_registration, name='employee_registration'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('Add_vendor/', views.Add_vendor, name='Add_vendor'),
    path('supplier_TBL/', views.supplier_TBL, name='supplier_TBL'),




]