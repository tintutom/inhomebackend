from rest_framework import serializers
from users.models import User,DoctorSlot,Payments,UserAddress,Feedback
from doctors.serializers import Doctorinfo_Serializer,Specialization_serializer
from doctors.models import Doctorinfo
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'
        
class User_Serializer(serializers.ModelSerializer):
    address=UserAddressSerializer(read_only=True)
    class Meta:
        model = User
        fields = '__all__'

class DoctorSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSlot
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time']
    
class DoctorSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSlot
        fields = '__all__'
       
class ProfessionalSerializer(serializers.ModelSerializer):
    user = Doctorinfo_Serializer(read_only=True) 
    category = Specialization_serializer(required=False) 

class BookingSerializer(serializers.ModelSerializer):
    # doctor = Doctorinfo_Serializer()
    # user =  User_Serializer()
    # docslot = DoctorSlotSerializer()
    class Meta:
        model = Payments
        fields = '__all__'
        
   
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['user', 'doctor', 'rating', 'review_text']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'userimage']       
class FeedbackListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
        
class PaymentSerializer(serializers.ModelSerializer):
    doctor = Doctorinfo_Serializer(read_only=True)
    user = User_Serializer(read_only=True)
    class Meta:
        model = Payments
        fields = '__all__'