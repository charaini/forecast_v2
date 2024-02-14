from drf_yasg import openapi
from rest_framework import status

weather_response_get = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'dates': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'min': openapi.Schema(type=openapi.TYPE_STRING),
                'max': openapi.Schema(type=openapi.TYPE_STRING),
                'current': openapi.Schema(type=openapi.TYPE_STRING),
            }),
            'cities': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'city': openapi.Schema(type=openapi.TYPE_STRING),
                'temp': openapi.Schema(type=openapi.TYPE_NUMBER),
                'precipitation': openapi.Schema(type=openapi.TYPE_STRING),
                'precipitation_probability': openapi.Schema(type=openapi.TYPE_INTEGER),
                'icon': openapi.Schema(type=openapi.TYPE_STRING),
            }),
        }
    ),
}

weather_response_post = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'city': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'is_favorite': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            }),
            'temp': openapi.Schema(type=openapi.TYPE_NUMBER),
            'precipitation': openapi.Schema(type=openapi.TYPE_STRING),
            'icon': openapi.Schema(type=openapi.TYPE_STRING),
            'date': openapi.Schema(type=openapi.TYPE_STRING),
            'precipitation_probability': openapi.Schema(type=openapi.TYPE_INTEGER),
            'precipitation_probability_ai': openapi.Schema(type=openapi.TYPE_INTEGER)
        }
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
}

city_response_get = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    ),
}

city_response_post = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
}

graph_response_get = {
    status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'accuracy': openapi.Schema(type=openapi.TYPE_NUMBER),
                'predictions_count': openapi.Schema(type=openapi.TYPE_NUMBER),
            }
    ),
}

prediction_response_get = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'predictions': openapi.Schema(type=openapi.TYPE_ARRAY,
                                          items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                              'city': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                                  'name': openapi.Schema(type=openapi.TYPE_STRING),
                                                  'is_favorite': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                              }),
                                              'temp': openapi.Schema(type=openapi.TYPE_NUMBER),
                                              'precipitation': openapi.Schema(type=openapi.TYPE_STRING),
                                              'icon': openapi.Schema(type=openapi.TYPE_STRING),
                                              'date': openapi.Schema(type=openapi.TYPE_STRING),
                                              'precipitation_probability': openapi.Schema(type=openapi.TYPE_INTEGER),
                                              'precipitation_probability_ai': openapi.Schema(type=openapi.TYPE_INTEGER)
                                          })),
            'dates': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'min': openapi.Schema(type=openapi.TYPE_STRING),
                'max': openapi.Schema(type=openapi.TYPE_STRING),
                'current': openapi.Schema(type=openapi.TYPE_STRING),
            }),
        }
    ),
}
