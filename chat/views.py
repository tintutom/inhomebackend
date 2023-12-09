# # chat/views.py
# from django.http import JsonResponse

# def websocket_url(request, sender_id, receiver_id):
#     websocket_url = f"ws://{request.get_host()}/ws/chat/{sender_id}/{receiver_id}/"
#     print(websocket_url,"socketttttttttttttttttttt")
#     return JsonResponse({'websocket_url': websocket_url})
# print("...............................")


# Create a new Django REST API view
# chat/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatMessage

class ExistingMessagesView(APIView):
    def get(self, request, appointment_id):
        messages = ChatMessage.objects.filter(appointment_id=appointment_id).order_by('timestamp')
        data = [
            {
                'message': message.message,
                'sender' : message.sender.name,
                'sender_id': message.sender.id,
                'reciever' : message.receiver.name,
                'receiver_id': message.receiver.id,
                'timestamp' : message.timestamp            
            } 
            
            for message in messages
        ]
        return Response(data)
