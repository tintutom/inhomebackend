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
        fields = '__all__'

        # fields = ['experience', 'education', 'current_working_hospital', 'fee', 'gender']
class DoctorAdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAdditionalDetails
        # fields = '__all__'

        fields = ['experience', 'education', 'current_working_hospital', 'fee', 'gender']


class Doctorinfo_Serializer(serializers.ModelSerializer):
    specialization = Specialization_serializer(required=False)
    additional_details = DoctorAdditionalDetailsSerializer()

    class Meta:
        model = Doctorinfo
        exclude = ['password']
        
    def update(self, instance, validated_data):
        additional_details_data = validated_data.pop('additional_details', {})
        additional_details_instance = instance.additional_details

        for key, value in additional_details_data.items():
            setattr(additional_details_instance, key, value)

        # Update Doctorinfo fields
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # Save changes to both models
        instance.save()
        additional_details_instance.save()

        return instance

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


      


        