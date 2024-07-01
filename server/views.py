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
    visitor_name = request.GET.get("visitor_name", "Guest")
    client_ip = get_client_ip(request)

    api_key = "at_IZZho0iOix69h2SEo6ClSJCrFO87D"

    try:
        response = requests.get(
            f"https://geo.ipify.org/api/v2/country?apiKey={api_key}&ipAddress={client_ip}"
        )
        data = response.json()
        region = data.get("region", "Unknown")
    except requests.exceptions.RequestException as e:
        location = "Unknown"

    temperature = "11 Degrees Celsius"
    greeting = f"Hello {visitor_name}, your location is {location} and the temperature is {temperature}"

    return JsonResponse(
        {"Client_ip": client_ip, "Location": region, "Greeting": greeting}
    )
