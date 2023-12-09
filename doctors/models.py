from django.db import models

class Specialization(models.Model):
    specialization = models.CharField(max_length=100)
    
    def __str__(self):
        return self.specialization
    
class Doctorinfo(models.Model):

    name = models.CharField(max_length=150)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=30)
    admin_position = models.CharField(max_length=30)
    specialization=models.ForeignKey(Specialization,on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    image = models.ImageField( upload_to='images',null=True,blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)



class DoctorAdditionalDetails(models.Model):
    doctor = models.OneToOneField(Doctorinfo, on_delete=models.CASCADE, related_name='additional_details')
    experience = models.IntegerField()  # Years of experience
    education = models.TextField()  # Education details (multiple values if needed)
    current_working_hospital = models.CharField(max_length=150)
    latitude=models.DecimalField(max_digits=30,decimal_places=20, null=True,blank=True)
    longitude=models.DecimalField(max_digits=30,decimal_places=20, null=True,blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)  # Decimal field for the fee
    gender = models.CharField(max_length=10)  

    def __str__(self):
        return f"{self.doctor.name}'s Additional Details"



class DoctorSlot(models.Model):
    doctor = models.ForeignKey(Doctorinfo, on_delete=models.CASCADE,related_name='slot')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)


    def __str__(self):
        availability = 'Available' if self.is_available else 'Booked'
        return f"{self.doctor.name}'s Slot on {self.date} - {self.start_time} to {self.end_time}"


