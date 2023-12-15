from django.contrib import admin
from .models import Specialization,Doctorinfo,DoctorAdditionalDetails
admin.site.register(Doctorinfo)
admin.site.register(DoctorAdditionalDetails)
admin.site.register(Specialization)