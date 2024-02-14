from django.contrib import admin

from .models import City, Predictions, PrecipitationType


admin.site.register(City)
admin.site.register(Predictions)
admin.site.register(PrecipitationType)
