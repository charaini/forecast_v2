from django.db import models
from django.contrib.auth import get_user_model


class City(models.Model):
    name = models.CharField(max_length=30)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    is_favorite = models.BooleanField(default=False, verbose_name='Избранное')

    def __str__(self):
        return f'{self.id}. {self.name}'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class PrecipitationType(models.Model):
    name = models.CharField(max_length=62)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип осадков'
        verbose_name_plural = 'Типы осадков'


class Predictions(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='predictions')
    city_id = models.ForeignKey('City', on_delete=models.CASCADE)
    date = models.DateField()
    precipitation_type = models.ForeignKey('PrecipitationType', on_delete=models.CASCADE)
    precipitation_probability = models.FloatField(verbose_name='Вероятность осадков')
    precipitation_probability_ai = models.FloatField(verbose_name='Вероятность осадков от ИИ')

    def __str__(self):
        return f'Прогноз №{self.id}'

    class Meta:
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'
