from rest_framework import serializers
from users.models import Payments, Feedback
from doctors.models import Doctorinfo
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctorinfo
        fields = '__all__'
        
class FeedbackSerializer(serializers.ModelSerializer):
    doctor=DoctorSerializer()
    class Meta:
        model = Feedback
        fields = '__all__'
    
