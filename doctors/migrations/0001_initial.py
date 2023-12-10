# Generated by Django 5.0 on 2023-12-09 05:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctorinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=30)),
                ('admin_position', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=13)),
                ('email', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorAdditionalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.IntegerField()),
                ('education', models.TextField()),
                ('current_working_hospital', models.CharField(max_length=150)),
                ('latitude', models.DecimalField(blank=True, decimal_places=20, max_digits=30, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=20, max_digits=30, null=True)),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('gender', models.CharField(max_length=10)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='additional_details', to='doctors.doctorinfo')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slot', to='doctors.doctorinfo')),
            ],
        ),
        migrations.AddField(
            model_name='doctorinfo',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctors.specialization'),
        ),
    ]