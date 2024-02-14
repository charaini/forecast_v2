import json
import random
from typing import Tuple

import requests
from datetime import datetime, timedelta

from .models import City

from .config import API_KEY, API_URL, API_HISTORY_URL, API_FUTURE_URL

weather_precipitation = {
    'snow': 'снег',
    'no precipitation': 'нет',
    'rain or snow': 'дождь или снег',
    'rain': 'дождь'
}


def get_probability_and_precip_from_json(weather_data: dict, date: datetime.date = None) -> Tuple[int, str]:
    code = weather_data["condition"]["code"]
    weather_obj = {}

    now = datetime.now()
    if date is not None:
        find_date = datetime.strptime(date, '%Y-%m-%d')
        date_difference = find_date - now
        if not date_difference > timedelta(days=13) and not now - timedelta(days=1) > find_date:
            return calculate_prob_of_precip_and_precip(weather_data)

    with open('weather/codeweather.json', encoding='utf-8') as f:
        codes_objects = json.load(f)
        for code_obj in codes_objects:
            if code_obj["code"] == code:
                weather_obj = code_obj
                break

    precipitation = weather_precipitation[weather_obj["group"]]
    if precipitation == 'нет':
        day_probability = 0
    else:
        day_probability = random.randint(weather_obj["day_probability"][0], weather_obj["day_probability"][1])

    return day_probability, precipitation


def calculate_prob_of_precip_and_precip(weather_data: dict) -> Tuple[int, str]:
    chance_of_rain = weather_data["daily_chance_of_rain"]
    chance_of_snow = weather_data["daily_chance_of_snow"]

    probability_of_precipitation = round(100 - (100 - chance_of_rain) * (100 - chance_of_snow) / 100)

    precipitation = 'нет'
    if chance_of_rain and chance_of_snow:
        precipitation = 'дождь или снег'
    elif chance_of_rain:
        precipitation = 'дождь'
    elif chance_of_snow:
        precipitation = 'снег'

    return probability_of_precipitation, precipitation


def get_date_title(date: datetime.date) -> str:
    month_titles = {
        1: 'Января',
        2: 'Февраля',
        3: 'Марта',
        4: 'Апреля',
        5: 'Мая',
        6: 'Июня',
        7: 'Июля',
        8: 'Августа',
        9: 'Сентября',
        10: 'Октября',
        11: 'Ноября',
        12: 'Декабря',
    }

    return f'{date.day} {month_titles[date.month]}'


def get_dates() -> dict:
    current_date = datetime.now().date()
    min_date = (current_date - timedelta(days=365)).strftime("%Y-%m-%d")
    max_date = (current_date + timedelta(days=299)).strftime("%Y-%m-%d")

    date = {
        'current': current_date.strftime("%Y-%m-%d"),
        'min': min_date,
        'max': max_date,
    }

    return date


def get_cities_info(request):
    cities = City.objects.filter(user_id=request.user.id).order_by('-id')
    cities_info = []
    is_error = False

    for city in cities:
        city_url = API_URL % (API_KEY, city, 1)
        try:
            res = requests.get(city_url)
            result = res.json()
            weather_data = result['forecast']['forecastday'][0]['day']

            prob_precipitation, precipitation = get_probability_and_precip_from_json(weather_data)

            city_info = {
                'city': city.name,
                'temp': result['current']['temp_c'],
                'precipitation': precipitation,
                'prob_precipitation': prob_precipitation,
                'icon': result['current']['condition']['icon']
            }

        except Exception as ex:
            print(f'Exception: {ex}')
            is_error = True
        else:
            cities_info.append(city_info)

    return cities_info, is_error


def convert_date(date: str) -> datetime.date:
    original_date = datetime.strptime(date, "%Y-%m-%d")
    return original_date


def find_forecast_day(date: str, city: str):
    url = API_URL % (API_KEY, city, 14)

    now = datetime.now()
    find_date = datetime.strptime(date, '%Y-%m-%d')
    date_difference = find_date - now
    if (now > find_date and
            not (now.day == find_date.day and now.month == find_date.month and now.year == find_date.year)):
        url = API_HISTORY_URL % (API_KEY, city, date)
    elif date_difference > timedelta(days=13):
        url = API_FUTURE_URL % (API_KEY, city, date)

    res = requests.get(url)
    result = res.json()

    forecast_days = result.get('forecast', '')
    if not forecast_days:
        return None
    forecast_days = forecast_days['forecastday']

    for day in forecast_days:
        if day['date'] == date:
            return day['day']
