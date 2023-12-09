from django.urls import path
from doctors import views
from doctors.views import *

urlpatterns = [
    path('doctor-info/<int:doctor_id>', DoctorInfoView.as_view(), name='doctor-info'),


    # path('<int:id>',views.Counts,name='hospitaldash'),
    path('signup',views.Sign_up.as_view(),name='signup'),
    path('login',views.Login.as_view(),name='login'),
    path('logout',views.DoctorLogout.as_view(),name='login'),
    path('verifyToken', views.verifyToken, name='verifyToken'),
    path('<int:doctor_id>/additional-details', DoctorAdditionalDetailsAPIView.as_view(), name='add-doctor-additional-details'),
    path('update/<int:doctor_id>/', DoctorInfoUpdateAPIView.as_view(), name='update-doctor-info'),

    path('<int:doctor_id>/slots', views.AddDoctorSlot.as_view(), name='doctor-slots'),
    path('view_slots/<int:doctor_id>', DoctorSlotsList.as_view(), name='doctor-slots-list'),
    path('<int:doctor_id>/view_slots', DoctorSlotsList.as_view(), name='doctor-slots-list'),
    path('<int:doctor_id>/slots/<int:slot_id>/update', views.UpdateDoctorSlot.as_view(), name='update-doctor-slot'),
    path('<int:doctor_id>/slots/<int:slot_id>/delete', views.DeleteDoctorSlot.as_view(), name='delete-doctor-slot'),
    # path('availability-list/<int:doctor_id>/', ProfessionalAvailabilityView.as_view(), name='availability-list'),
    path('upcoming-appointments/<int:doctor_id>/', UpcomingAppointmentsView.as_view(), name='upcoming-appointments'),



]