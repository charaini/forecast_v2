from drf_yasg import openapi
from rest_framework import status

user_response_get = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    ),
}
user_response_put = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        }
    ),
}
