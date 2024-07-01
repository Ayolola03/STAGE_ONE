from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.


@api_view(["GET"])
def hello(request):
    visitor_name = request.GET.get("visitor_name", "Guest")
    client_ip = request.META.get("REMOTE_ADDR")

    response = requests.get(f"http://ip-api.com/json/{client_ip}")
    data = response.json()
    location = data.get("city", "Unknown")
    temperature = "11 Degress Celsuis"
    greeting = f"Hello {visitor_name}, your location is {location} and the temperature is {temperature}"

    return JsonResponse(
        {"client_ip": client_ip, "location": location, "greeting": greeting}
    )
