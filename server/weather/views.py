from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .graph_service import filter_predictions_and_sort_by_dates, create_graph, create_pdf
from .models import City, Predictions, PrecipitationType
from .neiron.prediction import get_probability_from_ai
from .serializers import CitySerializer, PredictionSerializer, WeatherSerializer
from .services import get_dates, get_cities_info, find_forecast_day, get_probability_and_precip_from_json, convert_date
from .yasg_schemas import weather_response_post, weather_response_get, city_response_get, city_response_post, \
    graph_response_get, prediction_response_get


# Следующие принципы подходят для этих API классов.
# SOLID SRP - методы класса выполняют только свою функцию (по типу запроса: POST, GET, DELETE), и нет лишний работы.
# SOLID LSP - вместо реализации своих методов get, post и т.д мы используем методы
# класса от которых наследуемся, не ломая его. Наследуемся от тех классов, которые нам необходимы

# Принцип KISS
# Один из примеров в graph_service.py

class WeatherApi(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=weather_response_get)
    def get(self, request):
        """Получение погоды в городах"""
        # DRY - создана функция get_dates для не повторения кода.
        dates = get_dates()
        cities, is_error = get_cities_info(request)

        data = {'dates': dates, 'cities': cities}
        if is_error:
            data['error_message'] = 'Произошла ошибка при получении данных о погоде'

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=WeatherSerializer, responses=weather_response_post)
    def post(self, request):
        """Создание нового запроса на получение погоды по городу и дате"""
        city = request.data.get('city')
        date = request.data.get('date')

        # Проверка weather_data на пустые значения
        weather_data = find_forecast_day(date, city)
        if weather_data is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        prob_precipitation, precipitation = get_probability_and_precip_from_json(weather_data, date)
        prob_precipitation_ai = get_probability_from_ai(city, convert_date(date))
        city_obj = City.objects.get_or_create(name=city, user_id=request.user)[0]

        # DRY - вынос общих данных в отдельный массив
        total_info = {
            'date': date,
            'precipitation_probability': prob_precipitation,
            'precipitation_probability_ai': prob_precipitation_ai
        }

        Predictions.objects.create(
            user_id=request.user,
            city_id=city_obj,
            precipitation_type=PrecipitationType.objects.get(name=precipitation),
            **total_info,
        )

        weather = {
            'city': {
                'name': city,
                'is_favorite': city_obj.is_favorite
            },
            'temp': weather_data['avgtemp_c'],
            'precipitation': precipitation,
            'icon': weather_data['condition']['icon'],
            **total_info,
        }
        data = {'prediction': weather}
        return Response(data, status=status.HTTP_200_OK)


class CityApi(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=city_response_get)
    def get(self, request):
        """Получение городов в избранном"""
        city_id = request.GET.get('city_id', '')
        if city_id:
            city = City.objects.get(id=city_id)
            serializer = CitySerializer(instance=city)
        else:
            cities = City.objects.filter(user_id=request.user, is_favorite=True)
            serializer = CitySerializer(instance=cities, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CitySerializer, responses=city_response_post)
    def post(self, request):
        """Добавление города в избранное"""
        city = request.data.get('city')
        city_obj = City.objects.get(user_id=request.user, name=city)
        city_obj.is_favorite ^= True
        city_obj.save()

        if city_obj.is_favorite:
            message = f'Вы добавили в избранное город {city}'
        else:
            message = f'Вы удалили из избранного город {city}'

        return Response({'message': message}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Удаление города"""
        City.objects.get(id=pk, user_id=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class PredictionApi(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses=prediction_response_get)
    def get(self, request):
        """Получение всех прогнозов"""
        city_id = request.GET.get('city_id', '')
        date = request.GET.get('date', '')
        predictions_list = Predictions.objects.filter(user_id=request.user)

        # filtering data
        if date or city_id:
            if date:
                predictions_list = predictions_list.filter(date=date)
            if city_id:
                predictions_list = predictions_list.filter(city_id__id=city_id)
            if not predictions_list.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PredictionSerializer(instance=predictions_list, many=True)
        # DRY - создана функция get_dates для не повторения кода.
        return Response({'predictions': serializer.data, 'dates': get_dates()}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Удаление прогноза по id"""
        prediction = Predictions.objects.filter(id=pk, user_id=request.user)
        if not prediction.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        prediction.first().delete()
        return Response(status=status.HTTP_200_OK)


class GraphApi(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def generate_graph_and_get_accuracy(predictions) -> float:
        predictions = filter_predictions_and_sort_by_dates(predictions)

        dates = [prediction.date for prediction in predictions]
        probabilities = [prediction.precipitation_probability for prediction in predictions]
        probabilities_ai = [prediction.precipitation_probability_ai for prediction in predictions]

        accuracy = 0
        len_prob = len(probabilities)
        for i in range(len_prob):
            accuracy = round(sum(probabilities_ai) / sum(probabilities) * 100, 2)

        plot_file_path = create_graph(dates, probabilities, probabilities_ai)
        create_pdf(plot_file_path, f'Точность нейронной сети: {accuracy}', 'graph.pdf')
        return accuracy

    @swagger_auto_schema(responses=graph_response_get)
    def get(self, request):
        """Получение данных о графике"""
        if request.user.is_superuser:
            predictions = Predictions.objects.all()
        else:
            predictions = Predictions.objects.filter(user_id=request.user)
        if predictions.count() < 10:
            return Response({'message': 'Недостаточно запросов для формирования графика'},
                            status=status.HTTP_404_NOT_FOUND)

        accuracy = self.generate_graph_and_get_accuracy(predictions)
        return Response({'accuracy': accuracy, 'predictions_count': predictions.count()}, status=status.HTTP_200_OK)
