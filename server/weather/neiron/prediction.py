import datetime

from requests import get
import json
import pickle
import numpy as np
from datetime import timedelta

from weather.config import API_KEY


def get_probability_from_ai(city: str, date: datetime.date):
    prev_day = date - timedelta(days=1)
    current_day = date.today()

    try:
        response = json.loads(
            get(f'http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={city}&dt={date}').content.decode(
                'utf-8'))
        current_lst = response['forecast']['forecastday'][0]['day']
    except Exception:
        try:
            response = json.loads(
                get(f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=14&aqi=no&alerts=no').content.decode(
                    'utf-8'))

            current_lst = response['forecast']['forecastday'][(prev_day - current_day).days]['day']
        except Exception:
            response = json.loads(
                get(f'http://api.weatherapi.com/v1/future.json?key={API_KEY}&q={city}&dt={date.strftime("%Y-%m-%d")}').content.decode(
                    'utf-8'))
            current_lst = response['forecast']['forecastday'][0]['day']

    data_day = np.array([current_lst['maxtemp_c'], current_lst['mintemp_c'], current_lst['avgtemp_c'],
                         current_lst['maxwind_kph'], current_lst['totalprecip_mm'], current_lst['avgvis_km'],
                         current_lst['avghumidity']])

    with open('weather/neiron/best_model.pkl', 'rb') as f:
        model = pickle.load(f)

    return round(model.predict_proba([data_day])[0][0] * 100, 2)
