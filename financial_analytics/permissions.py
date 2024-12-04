# from rest_framework.permissions import BasePermission
# from rest_framework.exceptions import PermissionDenied
# from django.conf import settings
# import jwt

# class IsVendor(BasePermission):
#     def has_permission(self, request, view):
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return False  # Instead of raising an exception, return False

#         try:
#             # Extract the token
#             token = auth_header.split()[1]
            
#             # Decode the JWT using the secret key and algorithm from settings
#             decoded_token = jwt.decode(
#                 token,
#                 settings.JWT_SECRET_KEY,
#                 algorithms=[settings.JWT_ALGORITHM]
#             )
#             role = decoded_token.get('role')
#         except jwt.ExpiredSignatureError:
#             return False
#         except jwt.InvalidTokenError:
#             return False

#         # Check if the role matches 'VENDOR'
#         return role == "VENDOR"