from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('employee_registration/', views.employee_registration, name='employee_registration'),
    path('employee_list/', views.employee_list, name='employee_list'),



]
