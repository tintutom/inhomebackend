from django.urls import path
from users import views
from users.views import *

urlpatterns = [
    path('signup', views.Sign_up.as_view(), name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('verifyToken', views.verifyToken, name='verifyToken'),
    path('get-user/<int:id>', UserView.as_view(), name='get-user'),
    path('myprofile/<int:id>', views.myProfile, name="myprofile"),
    path('profileupdate/<int:id>', views.profileUpdate, name='profileUpdate'),
    path('changepassword/<int:id>', views.change_password, name='changepassword'),
    path('randomdoctor/', views.randomDoctor, name='randomDoctor'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('doctorsinfo/<int:specialization_id>/', DoctorListView.as_view(), name='doctor-list'),

    path('hospital_detail/<int:id>', views.randomDoctorInfo, name='hospital_detail'),
    path('all_slots/<int:doctor_id>/', AllSlotsAPIView.as_view(), name='all-slots'),
    path('available_slots/<int:doctor_id>', AvailableSlotsAPIView.as_view(), name='available_slots_api'),
    # path('book-appointment/<int:doctor_id>/<int:slot_id>', BookAppointmentAPIView.as_view(), name='book-appointment'),
    path('booked_slots/<int:doctor_id>', BookedSlotsAPIView.as_view(), name='booked-slots'),
    path('start_payment/<int:id>/', StartPaymentAPIView.as_view(), name='start_payment'),
    path('handle_payment_success/', HandlePaymentSuccessView.as_view(), name='handle_payment_success'),
    path('booking-update/', BookingCreateView.as_view(), name='booking-update'),
    
    path('useraddresses/<int:id>/', UserAddressListCreateView.as_view(), name='user-address-list-create'),
    path('user-addresses/<int:id>/', UserAddressUpdateView.as_view(), name='user-address-update'),
    path('upcoming-appointments/<int:id>/', UpcomingAppointmentsView.as_view(), name='upcoming-appointments'),
    path('cancel-appointment/', BookingCancelView.as_view(), name='cancel-appointments'),

    # path('user-past-appointments/<int:id>/', PastAppointmentsView.as_view(), name='user-past-appointments'),
    path('submit-feedback/', SubmitFeedbackView.as_view(), name='submit-feedback'),
    path('feedback-list/<int:doctor_id>/', FeedbackListView.as_view(), name='feedback-list'),
    path('feedback-list/', GeneralFeedbackListView.as_view(), name='feedback-list'),
    path('payment/', PaymentDetailView.as_view(), name='payment-detail'),

]