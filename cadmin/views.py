# from django.shortcuts import render
# from rest_framework.response import Response
# from users.models import User
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# import jwt
# from doctors.models import Hospital, Department,Doctor
# import json
# import base64
# from doctors.serializers import Hospital_Serializer, Department_serializer
# from users.serializers import User_Serializer
# from django.contrib.auth.hashers import check_password


# class Login(APIView):

#     def post(self, request):
#         try:
#             email = request.data['email']
#             password = request.data['password']

#         except:
#             return Response({'status': 'Please Give All Details'})

#         admin = User.objects.all()
#         status = 'None'

#         for i in admin:
#             if i.is_superuser:
#                 if i.email == email:
#                     if check_password(password, i.password):
#                         payload = {
#                             'email': email,
#                             'password': password
#                         }
#                         enpayload = base64.b64encode(json.dumps(
#                             payload).encode('utf-8')).decode('utf-8')
#                         jwt_token = jwt.encode(
#                             {'payload': enpayload}, 'secret', algorithm='HS256')
#                         response = Response(
#                             {'status': 'Success', 'payload': payload, 'jwt': jwt_token, 'role': 'admin'})

#                         return response

#                     else:
#                         status = 'Wrong Password'
#                         break
#                 else:
#                     status = 'Wrong Username'
#             else:
#                 status = 'Not A Admin Account'
#         return Response({'status': status})




# @api_view(['GET'])
# def User_details(request):
#     user = User.objects.all().order_by('id')
#     serializer = User_Serializer(user, many=True)
#     return Response(serializer.data)


# @api_view(['PUT'])
# def Block_user(request, id):
#     user = User.objects.get(id=id)
#     if user.is_active:
#         user.is_active = False
#         user.save()
#     else:
#         user.is_active = True
#         user.save()
#     return Response("Updated")


# @api_view(['GET'])
# def Counts(request):
#     hospital = Hospital.objects.filter(is_approved=True).count()
#     departments = Department.objects.all().count()
#     users = User.objects.all().count()
#     doctors = Doctor.objects.all().count()
#     return Response({'users':users,'hospital':hospital,'departments':departments,'doctors':doctors})

from django.shortcuts import render
from rest_framework.response import Response
from users.models import User,Feedback,Payments
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import jwt
from doctors.models import Doctorinfo, Specialization
import json
import base64
from doctors.serializers import Doctorinfo_Serializer,Specialization_serializer
from users.serializers import User_Serializer
from .serializers import FeedbackSerializer,AppointmentSerializer,DoctorSerializer
from django.contrib.auth.hashers import check_password


class Login(APIView):

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']

        except:
            return Response({'status': 'Please Give All Details'})

        admin = User.objects.all()
        status = 'None'

        for i in admin:
            if i.is_superuser:
                if i.email == email:
                    if check_password(password, i.password):
                        payload = {
                            'email': email,
                            'password': password
                        }
                        enpayload = base64.b64encode(json.dumps(
                            payload).encode('utf-8')).decode('utf-8')
                        jwt_token = jwt.encode(
                            {'payload': enpayload}, 'secret', algorithm='HS256')
                        response = Response(
                            {'status': 'Success', 'payload': payload, 'jwt': jwt_token, 'role': 'admin'})

                        return response

                    else:
                        status = 'Wrong Password'
                        break
                else:
                    status = 'Wrong Username'
            else:
                status = 'Not A Admin Account'
        return Response({'status': status})

class Logout(APIView):
    def get(self, request):
        response = Response({'status': 'success'})
        response.delete_cookie('jwt')
        return response
    
@api_view(['GET'])
def Hospital_details(request):
    hospital = Doctorinfo.objects.all().order_by('id')
    serializer = Doctorinfo_Serializer(hospital, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def Hospital_approval(request, id):
    hospital = Doctorinfo.objects.get(id=id)
    if hospital.is_approved:
        hospital.is_approved = False
        hospital.save()
    else:
        hospital.is_approved = True
        hospital.save()
    return Response("Updated")


@api_view(['DELETE'])
def Hospital_delete(request, id):
    hospital = Doctorinfo.objects.get(id=id)
    hospital.delete()
    return Response("Hospital Deleted")


class Department_add(APIView):
    def post(self, request):
        specialization = request.data.get('specialization')

        if specialization is None:
            return Response({'status': 'Please provide all details'})

        if len(specialization) < 3:
            return Response({'status': 'Name should be a minimum of 3 letters'})

        check_department = Specialization.objects.all()

        for i in check_department:
            if i.specialization == specialization:
                return Response({'status': 'Department already exists'})

        department = Specialization.objects.create(
            specialization=specialization,
        )
        department.save()
        return Response({'status': 'Success'})


@api_view(['GET'])
def Department_details(request):
    department = Specialization.objects.all().order_by('id')
    serializer = Specialization_serializer(department, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def Department_delete(request, id):
    department = Specialization.objects.get(id=id)
    department.delete()
    return Response("Department Deleted")


@api_view(['GET'])
def User_details(request):
    user = User.objects.all().order_by('id')
    serializer = User_Serializer(user, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def Block_user(request, id):
    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return Response("Updated")


@api_view(['GET'])
def Counts(request):
    # hospital = Hospital.objects.filter(is_approved=True).count()
    departments = Specialization.objects.all().count()
    users = User.objects.all().count()
    doctors = Doctorinfo.objects.all().count()
    return Response({'users':users,'departments':departments,'doctors':doctors})



@api_view(['GET'])
def departments(request,id):
    department = Specialization.objects.get(id=id)
    serializer = Specialization_serializer(department,many=False)
    return Response(serializer.data)

class AppointmentsAPIView(APIView):
    def get(self, request, format=None):
        appointments = Payments.objects.all()
        appointment_serializer = AppointmentSerializer(appointments, many=True)

        doctors = Doctorinfo.objects.all()
        doctor_serializer = DoctorSerializer(doctors, many=True)

        data = {
            'appointments': appointment_serializer.data,
            'doctors': doctor_serializer.data,
        }

        return Response(data)

class TopFeedbackAPIView(APIView):
    def get(self, request, format=None):
        top_feedback = Feedback.objects.order_by('-rating')[:5]
        serializer = FeedbackSerializer(top_feedback, many=True)
        return Response(serializer.data)

# from rest_framework import generics
# from cadmin.serializers import *
# from rest_framework import status
# from rest_framework.response import Response

# # Create your views here.

# class UserListView(generics.ListAPIView):
#     queryset = User.objects.filter(is_superuser=False, is_staff=False)
#     serializer_class = UserSerializer

# class ProfessionalListView(generics.ListAPIView):
#     queryset = Doctorinfo.objects.all()
#     serializer_class = ProfessionalSerializer