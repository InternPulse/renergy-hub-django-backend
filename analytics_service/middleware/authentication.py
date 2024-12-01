import jwt
import requests
from django.http import JsonResponse, HttpResponseForbidden
from decouple import config

JWT_SECRET_KEY = config('JWT_SECRET_KEY')
JWT_COOKIE_NAME = config('JWT_COOKIE_NAME')
EXTERNAL_VERIFY_URL = 'https://renergy-hub-express-backend.onrender.com/api/v1/auth/verify'

def get_jwt_from_cookies(request):
    token = request.COOKIES.get(JWT_COOKIE_NAME)
    print(f"All cookies: {request.COOKIES}")
    print(f"Token from cookies: {token}")
    return token

def verify_token_with_external_system(token):
    try:
        print(f"Sending verification request to: {EXTERNAL_VERIFY_URL}")
        response = requests.get(EXTERNAL_VERIFY_URL, params={'token': token}, timeout=5)
        print(f"External verification response: Status {response.status_code}, Body: {response.text}")
        response.raise_for_status()
        return response.status_code == 200, response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during external verification: {str(e)}")
        return False, {"message": "External verification failed"}

def jwt_middleware(get_response):
    def middleware(request):
        token = get_jwt_from_cookies(request)
        if not token:
            print("No token found in cookies.")
            return JsonResponse({'success': False, 'message': 'Authentication credentials were not provided.'}, status=401)

        try:
            # Verify the token externally
            is_valid, response_data = verify_token_with_external_system(token)
            if not is_valid:
                message = response_data.get('message', 'Invalid or expired token')
                print(f"Token validation failed: {message}")
                return JsonResponse({'success': False, 'message': message}, status=401)

            # If external verification succeeds, we can optionally decode the token
            try:
                decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
                print(f"Decoded token payload: {decoded_token}")

                # Check the role of the user (e.g., 'vendor')
                if decoded_token.get('role') == 'VENDOR':
                    request.jwt_payload = decoded_token
                    request.user = None  # Set to None or leave empty if no user model is tied
                else:
                    print(f"Access denied: User role is not VENDOR. Role: {decoded_token.get('role')}")
                    return HttpResponseForbidden('Access denied: Vendors only')
            except jwt.PyJWTError as jwt_error:
                print(f"JWT decoding error: {str(jwt_error)}")
                # Even if local decoding fails, we still proceed if external verification succeeded

        except Exception as e:
            print(f"Unexpected error in middleware: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Unexpected error occurred'}, status=500)

        return get_response(request)

    return middleware