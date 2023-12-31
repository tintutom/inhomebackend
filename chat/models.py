# chat/models.py
from django.db import models
from users.models import User,Payments
from doctors.models import Doctorinfo

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Doctorinfo, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    appointment = models.ForeignKey(Payments, on_delete=models.CASCADE, related_name='chat_messages', null=True)
    sendername = models.TextField(max_length=100, null=True,blank=True)
    
    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.message}'
