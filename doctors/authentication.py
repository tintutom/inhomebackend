
from rest_framework.response import Response
import jwt


def check_user(user, password, username,id):
    if user.is_approved and user.password == password:
        payload = {
            'username': username,
            'password': password,
            'id':id,
        }
        jwt_token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response({'status': 'Success', 'payload': payload, 'jwt': jwt_token, 'role': 'hospital','id':user.id})
        print(jwt_token)
    else:
        response = Response({'status': 'Authentication Failed'})

    return response
