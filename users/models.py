from datetime import datetime
from django.utils import timezone
from django.db import models
from doctors.models import Doctorinfo,DoctorSlot

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=13)
    password = models.CharField(max_length=5000)
    userimage = models.ImageField(upload_to='images/user_images/', null=True, blank=True)  # Specify the upload path
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)
    
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    address = models.TextField()
    latitude=models.DecimalField(max_digits=30,decimal_places=20, null=True)
    longitude=models.DecimalField(max_digits=30,decimal_places=20, null=True)
    
class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    doctor = models.ForeignKey(Doctorinfo, on_delete=models.CASCADE, related_name='bookings', null=True)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default='00:00:05')
    end_time = models.TimeField(default='00:00:05')
    documents = models.FileField(upload_to='documents/', null=True, blank=True)
    payment = models.BooleanField(default=False)
    amount = models.IntegerField()  
    doctor_slot = models.ForeignKey(DoctorSlot, on_delete=models.CASCADE,null=True)
    city = models.CharField(max_length=255, null=True)
    address = models.TextField(max_length=255,null=True)
    latitude=models.DecimalField(max_digits=30,decimal_places=20, null=True)
    longitude=models.DecimalField(max_digits=30,decimal_places=20, null=True)
    
  

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctorinfo, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.name} to Dr. {self.doctor.name}"
  