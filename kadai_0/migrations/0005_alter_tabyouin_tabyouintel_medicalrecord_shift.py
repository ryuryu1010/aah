# Generated by Django 5.0.6 on 2024-06-20 00:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kadai_0', '0004_alter_tabyouin_kyukyu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabyouin',
            name='tabyouintel',
            field=models.CharField(max_length=15),
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.TextField()),
                ('treatment_plan', models.TextField()),
                ('record_date', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kadai_0.employee')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kadai_0.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('role', models.CharField(max_length=32)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kadai_0.employee')),
            ],
        ),
    ]
