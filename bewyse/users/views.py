# from django.http import JsonResponse
# from rest_framework import status
# from rest_framework.decorators import api_view
# from .models import CustomUser
# from firebase_admin import auth
# from django.contrib.auth import authenticate
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import check_password

# from rest_framework.decorators import api_view
# from rest_framework import status
# from django.http import JsonResponse
# import firebase_admin
# from firebase_admin import auth
# import base64

# import jwt
# firebase_project_id = "bewyse-dc03c"
# import json
# from django.conf import settings


# import jwt
# import os
# from .models import CustomUser
# from .serializers import *

# from rest_framework.decorators import api_view
# from rest_framework import status
# from rest_framework.response import Response
# from .serializers import RegistrationSerializer
# from .models import CustomUser
# import firebase_admin
# from firebase_admin import auth

    
# from django.conf import settings
# from cryptography.hazmat.primitives import serialization

# from .firebase_middleware import FirebaseMiddleware  



# def create_custom_token(user_id):

#     custom_token = auth.create_custom_token(user_id)
#     return custom_token


# def get_public_key():

#     file_path = os.path.join(settings.BASE_DIR, 'bewyse', 'cred.json')
#     with open(file_path, "r") as f:
#         service_account_key_data = json.load(f)

#     private_key_pem = service_account_key_data['private_key']
#     private_key_bytes = private_key_pem.encode('utf-8')
#     private_key = serialization.load_pem_private_key(private_key_bytes, password=None)

#     public_key = private_key.public_key().public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo,
#     ).decode('utf-8')

#     return public_key


# def get_payload_by_id(custom_token):
#     public_key = get_public_key()

#     try:
#         decoded_token = jwt.decode(custom_token, public_key, algorithms=['RS256'], options={"verify_signature": False})
        
#         if decoded_token:
#             token_parts = custom_token.split(".")

#         if len(token_parts) >= 2:
#             encoded_token = token_parts[1]

#             encoded_token = encoded_token.replace("-", "+").replace("_", "/")
#             padding = 4 - (len(encoded_token) % 4)
#             encoded_token += "=" * padding
#             decoded_token = base64.b64decode(encoded_token).decode('utf-8')

#             payload_dict = json.loads(decoded_token)

#             uid = payload_dict.get("uid")
#             return uid

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# def your_custom_authentication_logic(email, password):
#     try:
#         user = CustomUser.objects.get(email=email)
#         if check_password(password, user.password):
#             return True  # Authentication successful
#     except CustomUser.DoesNotExist:
#         pass

#     return False  # Authentication failed

# def create_custom_token(user_id):
#     custom_token = auth.create_custom_token(user_id)
#     return custom_token



# @api_view(['POST'])
# def register_view(request):
#     serializer = RegistrationSerializer(data=request.data)

#     if serializer.is_valid():
#         username = serializer.validated_data['username']
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']
#         first_name = serializer.validated_data.get('first_name', '')
#         last_name = serializer.validated_data.get('last_name', '')

#         if CustomUser.objects.filter(username=username).exists():
#             return Response({'error': 'A user with that username already exists'}, status=status.HTTP_400_BAD_REQUEST)

#         if len(password) < 8:
#             return Response({'error': 'This password is too short. It must contain at least 8 characters'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

#             return Response({'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login_view(request):
#     if request.method == 'POST':

#         return JsonResponse({
#             'custom_token': request.custom_token
#         }, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def view_profile(request):
#     custom_token = request.META.get('HTTP_CUSTOM_TOKEN')

#     if not custom_token:
#         return Response({'error': 'Unauthorized. Custom token is required.'}, status=status.HTTP_401_UNAUTHORIZED)

#     try:

#         user_uid = get_payload_by_id(custom_token)
#         user = auth.get_user(user_uid)
#         user_email = user.email

#         user_info = CustomUser.objects.filter(email=user_email)

#         serializer = ViewProfile(user_info, many=True)
#         return Response(serializer.data)
#     except jwt.ExpiredSignatureError:
#         return Response({'error': 'Custom token has expired.'}, status=status.HTTP_401_UNAUTHORIZED)
#     except jwt.InvalidTokenError:
#         return Response({'error': 'Custom token is invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
# @api_view(['POST'])
# def edit_user_profile(request):
#     custom_token = request.META.get('HTTP_CUSTOM_TOKEN')

#     if not custom_token:
#         return Response({'error': 'Unauthorized. Custom token is required.'}, status=status.HTTP_401_UNAUTHORIZED)

#     if request.method == 'POST':

#         user_uid = get_payload_by_id(custom_token)
#         user = auth.get_user(user_uid)
#         user_email = user.email

#         try:
#             user = CustomUser.objects.get(email=user_email)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = UserProfileEditSerializer(user, data=request.data, partial=True)

#         if serializer.is_valid():
#             new_username = serializer.validated_data.get('username')
#             existing_user = CustomUser.objects.exclude(pk=user.id).filter(username=new_username)
#             if existing_user.exists():
#                 return Response({'error': 'User already exist with the username ' + new_username}, status=status.HTTP_400_BAD_REQUEST)

#             serializer.save()

#             return JsonResponse({
#                 'message': 'User profile updated successfully.',
#                 'data': serializer.data
#             }, status=status.HTTP_200_OK)
#         else:
#             return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)