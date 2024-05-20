# employee_management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin/home/', views.admin_home, name='admin_home'),
    path('reception/home/', views.reception_home, name='reception_home'),
    path('doctor/home/', views.doctor_home, name='doctor_home'),
]
