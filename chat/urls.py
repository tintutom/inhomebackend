from django.urls import path
from .views import ExistingMessagesView

urlpatterns = [
    path('<int:appointment_id>/', ExistingMessagesView.as_view(), name='existing_messages'),
]