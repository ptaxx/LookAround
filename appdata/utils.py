import requests
from django.conf import settings


def get_weather_data(area_id):
    url = f"http://api.openweathermap.org/data/2.5/weather?id={area_id}&appid=6fa3a061f537db1e424bfc7a15780d0d&units=metric"
    
    try:
        response = requests.get(url)  # No need to format the URL further
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)

        # Parse JSON content
        data = response.json()
        
        # Extract required fields
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
    
    
x = get_weather_data('588409')
print(x)