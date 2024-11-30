from datetime import datetime
import requests
from django.utils import timezone
from decouple import config


def get_weather_data(area_id):
    url = f"http://api.openweathermap.org/data/2.5/weather?id={area_id}&appid={config('API_KEY')}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  

        data = response.json()
        
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind': data['wind']['speed']
        }
        return weather

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except KeyError:
        print("Unexpected response structure")
        return None


def countdown_timer(date_time):
    now = timezone.now()
    if date_time > now:
        time_remaining = date_time - now
        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60
        seconds = time_remaining.seconds % 60
        time_data = {
            'game_started': False,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
        }
    else:
        time_remaining = now - date_time
        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60
        seconds = time_remaining.seconds % 60
        time_data = {
            'game_started': True,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
        }
    return time_data