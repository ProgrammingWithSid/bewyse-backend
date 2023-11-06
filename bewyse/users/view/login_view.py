
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from firebase_admin import auth
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
import firebase_admin
from firebase_admin import auth
import base64

import jwt
firebase_project_id = "bewyse-dc03c"

from users.models import *

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from users.serializers import RegistrationSerializer
import firebase_admin
from users.middlewares.login_middleware import LoginMiddleware

# login_view.py

from django.http import JsonResponse
from django.contrib.sessions.models import Session
from firebase_admin import auth

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        # Access custom_token from the session
        print("here")
        custom_token = request.session.get('custom_token')
        print(custom_token)

        if custom_token:
            return JsonResponse({
                'custom_token': custom_token
            }, status=200)
        else:
            return JsonResponse({'error': 'An error occurred during login.'}, status=500)

@api_view(['POST'])
def register_view(request):
    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        first_name = serializer.validated_data.get('first_name', '')  # Use get() with default value
        last_name = serializer.validated_data.get('last_name', '')  # Use get() with default value

        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'A user with that username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({'error': 'This password is too short. It must contain at least 8 characters'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,  # Provide the first_name value
                last_name=last_name  # Provide the last_name value
            )

            return Response({'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)