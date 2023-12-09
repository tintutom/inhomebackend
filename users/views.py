import datetime
from rest_framework.response import Response    
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from users.serializers import User_Serializer,DoctorSlotSerializer,BookingSerializer,FeedbackListSerializer
import jwt
from django.contrib.auth.hashers import make_password, check_password
import json
import base64
from doctors.models import Doctorinfo,Specialization,DoctorSlot,DoctorAdditionalDetails
from doctors.serializers import Specialization_serializer,DoctorAdditionalDetailsSerializer,Doctorinfo_Serializer,DoctorSlotSerializer
from rest_framework import status
from .models import  User,Payments,UserAddress,Feedback
from .serializers import User_Serializer,DoctorSlotSerializer,ProfessionalSerializer,UserAddressSerializer,FeedbackSerializer,PaymentSerializer
import razorpay
from datetime import datetime
from django.utils import timezone
from rest_framework import generics
from django.shortcuts import get_object_or_404



class Sign_up(APIView):
    def post(self, request):
        try:
            name = request.data['name']
            email = request.data['email']
            phone = request.data['phone']
            password = make_password(request.data['password'])
            userimage = request.data.get('photo') 
        except KeyError:
            return Response({'status': 'Please provide the required details (name, email, phone, password, and userimage)'})

        if len(name) < 3:
            return Response({'status': 'Name should be a minimum of 3 letters'})
        if len(password) < 5:
            return Response({'status': 'Password should be a minimum of 5 characters'})

        check_user = User.objects.filter(email=email).first()

        if check_user:
            return Response({'status': 'Email is already in use'})

        check_user = User.objects.filter(phone=phone).first()

        if check_user:
            return Response({'status': 'Phone number is already in use'})

        user = User.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=password,
            userimage=userimage, 
        )
        user.save()

        return Response({'status': 'Success'})


class Login(APIView):
    def post(self, request):

        try:
            email = request.data['email']
            password = str(request.data['password'])
        except:
            return Response({'status': 'Please Provide details(email,password)'})

        user = User.objects.all()
        status = 'None'

        for i in user:
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
                        {'status': 'Success', 'payload': enpayload, 'jwt': jwt_token, 'role': 'user', 'id': i.id})
                    return response
                else:
                    status = 'Wrong Password'
                    break
            else:
                status = 'Email is not found'

        return Response({'status': status})


class Logout(APIView):
    def get(self, request):
        response = Response({'status': 'success'})
        response.delete_cookie('jwt')
        return response


@api_view(['POST'])
def verifyToken(request):
    token = request.data.get('token')
    decoded = jwt.decode(token, 'secret', algorithms='HS256')
    # Decode  payload
    decoded_bytes = base64.b64decode(decoded['payload'])
    #  byte string to unicode string
    decoded_str = decoded_bytes.decode('utf-8')
    decoded1 = json.loads(decoded_str)  # Parse JSON string as dictionary
    user = User.objects.get(email=decoded1.get('email'))

    if user:
        return Response({'username': user.name, 'id': user.id})
    else:
        return Response({'status': 'Token InValid'})

from django.contrib.auth import authenticate
class LoginMachine(APIView):
    def post(self,request):
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            return Response("Please give all details")
        
        user = authenticate(username=username,password=password)
        if user is not None:
            payload={
                'username':username,
                "password":password
            }
            jwt_token = jwt.encode({'payload':payload},'secret',algorithm='HS256')
            response = Response({'status':'Logged','payload':payload,'jwt':jwt_token})
            return response
        else:
            return Response("Account not exist")

@api_view(['GET'])
def myProfile(request, id):
    user = User.objects.filter(id=id)
    serializer = User_Serializer(user, many=True)
    return Response(serializer.data)

class UserView(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = User_Serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
def profileUpdate(request, id):
    try:
        name = request.data['name']
        phone = request.data['phone']
        email = request.data['email']
    except:
        return Response('Please provide all details')

    user = User.objects.get(id=id)
    user.name = name
    user.email = email
    user.phone = phone
    user.save()

    return Response("Profile Updated Successfully")


@api_view(["PUT"])
def change_password(request, id):
    try:
        old = request.data['oldpassword']
        new = request.data['newpassword']
    except:
        return Response('Please Fill All Details')
    user = User.objects.get(id=id)
    if check_password(old, user.password):
        user.password = make_password(new)
        user.save()
        return Response("Password Updated")
    return Response("Old Password Is Wrong")

# show the admin approved dotors list
@api_view(["GET"])
def randomDoctor(request):
    doctor = Doctorinfo.objects.filter(is_approved=True)
    serializer = Doctorinfo_Serializer(doctor, many=True)
    return Response(serializer.data)

class CategoryListView(APIView):
    def get(self, request):
        categories = Specialization.objects.all()
        serializer = Specialization_serializer(categories, many=True)
        return Response({'categories': serializer.data})

# show doctors based on particular category 
class DoctorListView(APIView):
    def get(self, request, specialization_id):
        doctors = Doctorinfo.objects.filter(specialization=specialization_id,is_approved=True)
        serializer = Doctorinfo_Serializer(doctors, many=True)
        return Response({'doctors': serializer.data})

@api_view(["GET"])
def randomDoctorInfo(request,id):
    doctor = Doctorinfo.objects.get(id=id)
    serializer = Doctorinfo_Serializer(doctor)
    return Response(serializer.data)

class UserAddressListCreateView(APIView):
    def post(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            city = request.data['city']
            address = request.data['address']
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')
        except KeyError as e:
            return Response({'status': f'Missing field: {e}'}, status=400)

        address = UserAddress.objects.create(user=user, city=city, address=address, latitude=latitude, longitude=longitude,)

        # You can use a serializer to return the address details in the response if needed
        serializer = UserAddressSerializer(address)

        return Response({'status': 'Address added successfully', 'address': serializer.data})

class UserAddressUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    lookup_field = 'id'

class AllSlotsAPIView(APIView):
    def get(self, request, doctor_id):
        try:
            doctor_slots = DoctorSlot.objects.filter(doctor__id=doctor_id)
            serializer = DoctorSlotSerializer(doctor_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DoctorSlot.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

class AvailableSlotsAPIView(APIView):
    def get(self, request, doctor_id):
        try:
            doctor_slots = DoctorSlot.objects.filter(doctor__id=doctor_id,is_available=True)
            serializer = DoctorSlotSerializer(doctor_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DoctorSlot.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

class BookedSlotsAPIView(APIView):
    def get(self, request, doctor_id):
        try:
            doctor_slots = DoctorSlot.objects.filter(doctor__id=doctor_id)
            booked_slots = Payments.objects.filter(doctor_slot__in=doctor_slots)
            serializer = BookingSerializer(booked_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DoctorSlot.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
       
class StartPaymentAPIView(APIView):
    def post(self,request,id):
        amount = request.data['fee']
        client = razorpay.Client(auth=("rzp_test_w6JtyXoIdcYWS4", "nwY7nZXOqgd8TlRYUE1GIGQg"))

        payment = client.order.create({
        "amount": int(float(amount) * 100),  
        "currency": "INR",
        "payment_capture": "1"
         })
        try:
            data = {
                "payment": payment,
            }
            print("startpayment dtaat:",data)
            return Response(data)
        except :
            return Response({'error': 'Professional with the provided ID does not exist'})
        
class HandlePaymentSuccessView(APIView):
    def post(self, request):
        try:
            ord_id = ""
            raz_pay_id = "" 
            raz_signature = ""

            res = json.loads(request.data["response"])
            print(res, 'resssssssssssssss')
            print('11111111111')
            print(res)
            for key in res.keys():
                if key == 'razorpay_order_id':
                    ord_id = res[key]
                elif key == 'razorpay_payment_id':
                    raz_pay_id = res[key]
                elif key == 'razorpay_signature':
                    raz_signature = res[key]

            ord_id = res.get('razorpay_order_id', '')
            print(ord_id, '-------------------')
            if ord_id is None:
                raise ValueError("Missing 'razorpay_order_id' in the response")

            order = Payments.objects.get(id=int(ord_id))

            # we will pass this whole data in razorpay client to verify the payment
            data = {
                'razorpay_order_id': ord_id,
                'razorpay_payment_id': raz_pay_id,
                'razorpay_signature': raz_signature
            }
            print(data, "data of order")
            client = razorpay.Client(auth=("rzp_test_w6JtyXoIdcYWS4", "nwY7nZXOqgd8TlRYUE1GIGQg"))

            check = client.utility.verify_payment_signature(data)
            if check is None:
                return Response({'error': 'Something went wrong'})

            # Fetch the booking details based on the provided information
            order = Payments.objects.get(order_payment_id=ord_id)
            user_id = order.user.id
            doctor_id = order.doctor.id
            date = order.date
            start_time = order.start_time
            end_time = order.end_time

            # Check if the user already has an appointment for the selected slot
            existing_appointment = Payments.objects.filter(
                user_id=user_id,
                doctor_id=doctor_id,
                date=date,
                start_time=start_time,
                end_time=end_time,
                payment=True,
            ).exists()

            if existing_appointment:
                return Response({'error': 'User already has an appointment for the selected slot'})

            # Update the payment status
            order.payment = True
            order.save()

            # Update the slot availability to false
            slot = get_object_or_404(
                DoctorSlot,
                doctor_id=doctor_id,
                date=date,
                start_time=start_time,
                end_time=end_time,
            )
            slot.is_available = False
            slot.save()

            res_data = {
                'message': 'Payment successfully received!'
            }

        except Payments.DoesNotExist:
            return Response({'error': 'Booking does not exist'})

        except Exception as e:
            print(e)
            return Response({'error': 'An error occurred'})

        print("HandlePaymentSuccess", res_data)
        return Response(res_data)

    
class BookingCreateView(APIView):
    def post(self, request):
        print('initial')
        
        payment_data = {
            'user': request.data.get('user'),
            'doctor': request.data.get('doctor'),
            'date': request.data.get('date'),
            'start_time': request.data.get('start_time'),
            'end_time': request.data.get('end_time'),
            'amount': request.data.get('amount'),
            'payment': request.data.get('payment'),
            'doctor_slot': request.data.get('doctor_slot'),
            'city':request.data.get('city'),
            'address':request.data.get('address'),
            'latitude':request.data.get('latitude'),
            'longitude':request.data.get('longitude'),
        }
        print("paymentttttttt", payment_data)
        serializer = BookingSerializer(data=payment_data)
        if serializer.is_valid():
            booking = serializer.save()
            
            # Update the slot availability to True
            doctor_slot_id = request.data.get('doctor_slot')
            slot = get_object_or_404(DoctorSlot, id=doctor_slot_id)
            slot.is_available = False 
            slot.save()

            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingCancelView(APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')
        booking = get_object_or_404(Payments, id=booking_id)
        
        # Free up the booked slot
        if booking.doctor_slot:
            booking.doctor_slot.is_available = True
            booking.doctor_slot.save()
        
        # Delete the booking
        booking.delete()

        return Response({"message": "Appointment cancelled successfully."}, status=status.HTTP_200_OK)
class UpcomingAppointmentsView(APIView):
    def get(self, request, id):  
        try:
            user_appointments = Payments.objects.filter(user_id=id, payment=True)
            serializer = BookingSerializer(user_appointments, many=True)
            appointments_data = serializer.data
            for appointment_data in appointments_data:
                doctor_id = appointment_data['doctor']
                user_id = appointment_data['user']

                doctor_instance = Doctorinfo.objects.get(id=doctor_id)
                user_instance = User.objects.get(id=user_id)

                doctor_serializer = Doctorinfo_Serializer(doctor_instance)
                user_serializer = User_Serializer(user_instance)

                appointment_data['doctor'] = doctor_serializer.data
                appointment_data['user'] = user_serializer.data


            return Response(appointments_data, status=status.HTTP_200_OK)
        except Payments.DoesNotExist:
            return Response({"error": "Payments not found"}, status=status.HTTP_404_NOT_FOUND)

      
class PastAppointmentsView(APIView):
    def get(self, request, id):  
        try:
            user_past_appointments = Payments.objects.filter(user_id=id, payment=True, date__lt=timezone.now())

            serializer = BookingSerializer(user_past_appointments, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Payments.DoesNotExist:
            return Response({"error": "Payments not found"}, status=status.HTTP_404_NOT_FOUND)

class SubmitFeedbackView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FeedbackSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class FeedbackListView(APIView):
    def get(self, request, doctor_id, *args, **kwargs):
        feedback = Feedback.objects.filter(doctor=doctor_id)
        serializer = FeedbackListSerializer(feedback, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class GeneralFeedbackListView(APIView):
    def get(self, request):
        feedback = Feedback.objects.all()
        serializer = FeedbackListSerializer(feedback, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       

class PaymentDetailView(APIView):
    def get(self, request):
        try:
            payment = Payments.objects.all()
            serializer = PaymentSerializer(payment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Payments.DoesNotExist:
            return Response({"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
