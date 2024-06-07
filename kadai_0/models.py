from django.db import models

# Create your models here.
from django.db import models



# 他病院表

class Tabyouin(models.Model):
    tabyouinid = models.CharField(max_length=8, primary_key=True)
    tabyouinmei = models.CharField(max_length=64)
    abyouinaddress = models.CharField(max_length=64)
    tabyouintel = models.CharField(max_length=13)
    byouinshihonk = models.IntegerField()
    kyukyu = models.IntegerField()

# 仕入れ先表

class Shiiregyosha(models.Model):
    shiireid = models.CharField(max_length=8, primary_key=True)
    shiiremei = models.CharField(max_length=64)
    shiireaddress = models.CharField(max_length=64)
    shiiretel = models.CharField(max_length=15)
    shihonkin = models.IntegerField()
    nouki = models.IntegerField()

# 従業員表

class Employee(models.Model):
    empid = models.CharField(max_length=8, primary_key=True)
    empfname = models.CharField(max_length=64)
    empiname = models.CharField(max_length=64)
    emppasswd = models.CharField(max_length=64)
    emprole = models.IntegerField()

# 患者表

class Patient(models.Model):
    patid = models.CharField(max_length=8, primary_key=True)
    patfname = models.CharField(max_length=64)
    patiname = models.CharField(max_length=64)
    hokenmei = models.CharField(max_length=64)
    hokenexp = models.DateField()

# 薬剤表

class Medicine(models.Model):
    medicineid = models.CharField(max_length=8, primary_key=True)
    medicinename = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)




# 処置表

class Treatment(models.Model):
    treatmentid = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE, limit_choices_to={'emprole': 1})  # 医師ロールに制限
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    treatment_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
