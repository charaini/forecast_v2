from django.urls import path

from .views import RegisterApi, UserInfoApi

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('me/', UserInfoApi.as_view()),
]
