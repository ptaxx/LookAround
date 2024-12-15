from datetime import datetime
import requests
from django.utils import timezone
from decouple import config
from .models import ActivityCheck


def get_weather_data(area_id):
    url = f"http://api.openweathermap.org/data/2.5/weather?id={area_id}&appid={config('API_KEY')}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        weather = {
            "city": data.get("name"),
            "temperature": data.get("main", {}).get("temp"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind": data.get("wind", {}).get("speed"),
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
        days = time_remaining.days
        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60
        seconds = time_remaining.seconds % 60
        total_hours = days * 24 + hours
        time_data = {
            "game_started": False,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
        }
    else:
        time_remaining = now - date_time
        days = time_remaining.days
        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60
        seconds = time_remaining.seconds % 60
        total_hours = days * 24 + hours
        time_data = {
            "game_started": True,
            "hours": total_hours,
            "minutes": minutes,
            "seconds": seconds,
        }
    return time_data


def user_activity_check(user, activity):
    if user.is_authenticated:
        activitycheck = ActivityCheck.objects.filter(activity=activity, user=user)
        user_has_activity = any(entry.is_active for entry in activitycheck)
    else:
        user_has_activity = False
    return user_has_activity


def get_location():
    url = "http://ip-api.com/json/"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        location = {
            "lat": data.get("lat"),
            "lon": data.get("lon"),
        }
        return location

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except KeyError:
        print("Unexpected response structure")
        return None


def compare_location(lat, lon):
    your_latitude = get_location()
    if your_latitude.get("lat") == lat and your_latitude.get("lon") == lon:
        return True
    else:
        return False
