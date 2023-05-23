from django.urls import path
from .views import home

app_name = 'public'


urlpatterns = [
    path('', home, name='home')
]