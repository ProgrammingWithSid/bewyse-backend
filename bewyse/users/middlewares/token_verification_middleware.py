from django.http import JsonResponse
import base64
import firebase_admin
from firebase_admin import auth
import json
from django.conf import settings
from cryptography.hazmat.primitives import serialization
import os
import rsa
import time
import jwt
from rest_framework.response import Response
from rest_framework import status

import firebase_admin
from firebase_admin import credentials
from django.http import JsonResponse
from django.conf import settings
import os




def get_public_key():

    file_path = os.path.join(settings.BASE_DIR, 'bewyse', 'cred.json')
    with open(file_path, "r") as f:
        service_account_key_data = json.load(f)

    private_key_pem = service_account_key_data['private_key']
    private_key_bytes = private_key_pem.encode('utf-8')
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)

    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode('utf-8')

    return public_key

def verify_custom_token(custom_token):
    public_key = get_public_key()
    try:
        decoded_token = jwt.decode(custom_token, public_key, algorithms=['RS256'], options={"verify_signature": False})
        print(decoded_token,"   sid")
        if decoded_token:
            current_time = int(time.time())
            if 'exp' in decoded_token and decoded_token['exp'] >= current_time:
                return decoded_token
            else:
                # Token has expired
                return None
    except Exception as e:
        return None

class TokenVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # if not firebase_admin._apps:
        #     bewyse_json_path = os.path.join(settings.BASE_DIR, 'bewyse', 'cred.json')
        #     cred = credentials.Certificate(bewyse_json_path)
        #     print(bewyse_json_path)
        #     firebase_admin.initialize_app(cred)

    def __call__(self, request):
        if request.path in ['/accounts/profile/view/', '/accounts/profile/edit/']:
            # Check if the custom_token exists in the request header
            custom_token = request.META.get('HTTP_CUSTOM_TOKEN')
            # custom_token = base64.b64decode(custom_token.encode('utf-8'))
            
            print(custom_token)

            print("Received custom_token:", custom_token)
            if custom_token:
                # Verify the token
                
                decoded_token = verify_custom_token(custom_token)
                # decoded_token = auth.verify_id_token(custom_token)

                if decoded_token:
                    # Store the decoded token in the response header
                    response = self.get_response(request)
                    # print(decoded_token," satender")
                    request.META['HTTP_CUSTOM_TOKEN'] = decoded_token
                    print(decoded_token,"heeeeee")
                    return self.get_response(request)
                else:
                    response = Response({'error': 'Invalid token.'}, status=401)
            else:
                response = Response({'error': 'Token not found in the request header.'}, status=401)
        else:
            # For other paths, simply pass the request to the next middleware or view
            print("should not be called")
            return self.get_response(request)