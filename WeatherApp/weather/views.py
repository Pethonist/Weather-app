from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):
    appid = '98212b68f33bb19820d3682930b59621'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()

        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'feels_like': res['main']['feels_like'],
            'icon': res['weather'][0]['icon'],
            'description': res['weather'][0]['description'],
            'pressure': res['main']['pressure'],
            'temp_min': res['main']['temp_min'],
            'temp_max': res['main']['temp_max'],
            'humidity': res['main']['humidity'],
            'wind_speed': res['wind']['speed']
        }

        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)
