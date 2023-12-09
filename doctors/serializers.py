from rest_framework import serializers
from doctors.models import Doctorinfo,Specialization,DoctorAdditionalDetails,DoctorSlot


class DoctorinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctorinfo
        fields = '__all__'

class Specialization_serializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id','specialization']


class DoctorAdditionalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAdditionalDetails
        fields = ['experience', 'education', 'current_working_hospital', 'fee', 'gender']


class Doctorinfo_Serializer(serializers.ModelSerializer):
    specialization = Specialization_serializer(required=False)
    additional_details = DoctorAdditionalDetailsSerializer()

    class Meta:
        model = Doctorinfo
        exclude = ['password']

class DoctorSlotSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    class Meta:
        model = DoctorSlot
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time','status']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data
    def get_status(self, obj):
        return 'Available' if obj.is_available else 'Booked'


      


        