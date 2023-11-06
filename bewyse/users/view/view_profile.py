from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from firebase_admin import auth
import jwt
from users.models import CustomUser
from users.serializers import ViewProfile
from rest_framework.response import Response
import base64
import json
from users.serializers import UserProfileEditSerializer

@api_view(['GET'])
def view_profile(request):
    print("INt")
    try:
        custom_token = request.META.get('HTTP_CUSTOM_TOKEN') 
        if not custom_token:
            return Response({'error': 'Unauthorized. Custom token is required in the header.'}, status=status.HTTP_401_UNAUTHORIZED)

        # payload_dict = json.loads(base64.b64decode(custom_token).decode('utf-8'))

        # payload_dict = jwt.decode(custom_token, verify=False)
        # print(payload_dict," hhhhhh")

        user_uid = custom_token.get("uid")
        user = auth.get_user(user_uid)
        user_email = user.email

        user_info = CustomUser.objects.filter(email=user_email)

        serializer = ViewProfile(user_info, many=True)
        return Response(serializer.data)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Custom token has expired.'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({'error': 'Custom token is invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['POST'])
def edit_user_profile(request):
    custom_token = request.META.get('HTTP_CUSTOM_TOKEN')

    if not custom_token:
        return Response({'error': 'Unauthorized. Custom token is required.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'POST':

        payload_dict = json.loads(base64.b64decode(custom_token.encode('utf-8')).decode('utf-8'))
        print(payload_dict)

        # payload_dict = jwt.decode(custom_token, verify=False)
        
        user_uid = payload_dict.get("uid")
        print(user_uid)
        user = auth.get_user(user_uid)
        user_email = user.email

        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileEditSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            new_username = serializer.validated_data.get('username')
            existing_user = CustomUser.objects.exclude(pk=user.id).filter(username=new_username)
            if existing_user.exists():
                return Response({'error': 'User already exist with the username ' + new_username}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return JsonResponse({
                'message': 'User profile updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)