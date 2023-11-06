from firebase_admin import credentials, auth, initialize_app
from django.http import JsonResponse
from django.conf import settings
import os



# Initialize Firebase Admin SDK
bewyse_json_path = os.path.join(settings.BASE_DIR, 'bewyse', 'cred.json')
cred = credentials.Certificate(bewyse_json_path)
print(bewyse_json_path)
firebase_app = initialize_app(cred)

class FirebaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        id_token = request.META.get('HTTP_FIREBASE_ID_TOKEN')
        print("c")
        print(id_token)
        if id_token:
            try:
                decoded_token = auth.verify_id_token(id_token)
                request.user = decoded_token
            except auth.ExpiredIdTokenError:
                return JsonResponse({'error': 'Custom token has expired'}, status=401)
            except auth.InvalidIdTokenError:
                return JsonResponse({'error': 'Custom token is invalid'}, status=401)

        response = self.get_response(request)
        return response
