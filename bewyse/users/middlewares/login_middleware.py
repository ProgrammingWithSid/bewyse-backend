from django.http import JsonResponse
from users.models import CustomUser
from firebase_admin import auth
from django.contrib.auth.hashers import check_password
import json
import base64
import firebase_admin
from firebase_admin import credentials
from django.http import JsonResponse
from django.conf import settings
import os

bewyse_json_path = os.path.join(settings.BASE_DIR, 'bewyse', 'cred.json')
cred = credentials.Certificate(bewyse_json_path)
print(bewyse_json_path)
firebase_admin.initialize_app(cred)


class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        

    def __call__(self, request):
        if request.path == '/accounts/login/' and request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')

            if your_custom_authentication_logic(email, password):
                print("yes")
                try:
                    user = auth.get_user_by_email(email)
                    print(f"Firebase user already exists: {user.uid}")
                except auth.UserNotFoundError:
                    firebase_user = auth.create_user(
                        email=email,
                        password=password,
                    )
                    print(f"Firebase user created: {firebase_user.uid}")

                custom_token = auth.create_custom_token(user.uid)
                custom_token_str = custom_token.decode('utf-8')  # Convert bytes-like object to a string
                request.session['custom_token'] = custom_token_str

            else:
                return JsonResponse({'error': 'Username or password is invalid.'}, status=401)

        response = self.get_response(request)
        return response

def your_custom_authentication_logic(email, password):
    try:
        user = CustomUser.objects.get(email=email)
        if check_password(password, user.password):
            return True  # Authentication successful
        else:
            print("Password authentication failed")
    except CustomUser.DoesNotExist:
        print("User does not exist")

    return False  # Authentication failed
