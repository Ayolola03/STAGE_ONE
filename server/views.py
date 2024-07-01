from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@api_view(["GET"])
def hello(request):
    visitor_name = request.GET.get("visitor_name")
    client_ip = get_client_ip(request)

    # Replace with your Geo.ipify API key
    api_key = "at_IZZho0iOix69h2SEo6ClSJCrFO87D"
    geo_url = f"https://geo.ipify.org/api/v1?apiKey={api_key}&ipAddress={client_ip}"

    try:
        # Fetch location data using Geo.ipify
        response_geo = requests.get(geo_url)
        response_geo.raise_for_status()
        data_geo = response_geo.json()
        location = f"{data_geo.get('location', {}).get('region', 'Unknown')}, {data_geo.get('location', {}).get('country', 'Unknown')}"

        # Fetch weather data using OpenWeatherMap
        weather_api_key = "1c56e2d2a1dcda840a5183eec122b8b2"
        lat = data_geo.get("location", {}).get("lat")
        lon = data_geo.get("location", {}).get("lng")
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"

        response_weather = requests.get(weather_url)
        response_weather.raise_for_status()
        data_weather = response_weather.json()
        temperature = data_weather.get("main", {}).get("temp", "Unknown")
    except requests.exceptions.RequestException as e:
        location = "Unknown"
        temperature = "Unknown"

    greeting = f"Hello {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"

    return JsonResponse(
        {"client_ip": client_ip, "location": location, "greeting": greeting}
    )
