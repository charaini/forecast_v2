import os

from fpdf import FPDF
from datetime import datetime
from typing import Union, List

import matplotlib
from django.db.models import QuerySet, Q

from matplotlib import pyplot as plt

from .models import Predictions

matplotlib.use('Agg')

months_dict = {
    'Jan': 'Янв',
    'Feb': 'Фев',
    'Mar': 'Мар',
    'Apr': 'Апр',
    'May': 'Май',
    'Jun': 'Июн',
    'Jul': 'Июл',
    'Aug': 'Авг',
    'Sep': 'Сен',
    'Oct': 'Окт',
    'Nov': 'Ноя',
    'Dec': 'Дек',
}


# KISS - У нас реализованы отдельные функции, как для создания графика, его сохранения, и создания pdf файла.
# Они выполняют свою логику, и не больше. Все просто реализовано.
def save_graph():
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    save_dir = os.path.join(static_dir, 'weather', 'img')
    os.makedirs(save_dir, exist_ok=True)

    plot_file_path = os.path.join(save_dir, 'plot.png')
    plt.savefig(plot_file_path)
    plt.close()
    return plot_file_path


def create_graph(dates, probabilities1, probabilities2) -> str:
    dates_temp = [date.strftime("%d %b") for date in dates]
    dates = []

    for date in dates_temp:
        for key, month in months_dict.items():
            if key in date:
                date = date.replace(key, month)
                dates.append(date)

    plt.figure(figsize=(9, 5))
    plt.plot(dates, probabilities1, marker='o', label='Прогнозы', color='blue')
    plt.plot(dates, probabilities2, marker='o', label='Прогнозы ИИ', color='orange')
    plt.xlabel('Даты')
    plt.ylabel('Вероятность осадков, %')
    plt.title('График вероятности осадков')
    plt.grid(True)
    plt.ylim(-2, 102)

    return save_graph()


def filter_predictions_and_sort_by_dates(predictions: Union[QuerySet, List[Predictions]]) -> list:
    predictions = predictions.filter(~Q(precipitation_type__name='нет'))

    temp_dates = []
    dates = []

    for prediction in predictions:
        if prediction.date not in temp_dates:
            temp_dates.append(prediction.date)
            dates.append(prediction)
    dates.sort(key=lambda x: datetime.strptime(x.date.strftime("%d %b"), "%d %b"))

    return dates


def create_pdf(image_path, text, output_path):
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    save_dir = os.path.join(static_dir, 'weather', 'graphs')

    pdf = FPDF()

    pdf.add_page()
    pdf.add_font('DejaVu', '', fr'{os.path.dirname(__file__)}\font\DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', size=25)

    pdf.cell(200, 10, txt=text, ln=1, align='C')
    pdf.image(image_path, x=-10, y=20, w=240, h=160)

    pdf.output(fr'{save_dir}\{output_path}')
