from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.


@api_view(["GET"])
def hello(request):
    visitor_name = request.GET.get("visitor_name", "Guest")
    client_ip = request.META.get("REMOTE_ADDR")

    response = requests.get(
        f"https://api.ipdata.co/{client_ip}?api-key="
    )
    data = response.json()
    location = data.get("city", "Unknown")
    temperature = "11 Degress Celsuis"
    greeting = f"Hello {visitor_name}, your location is {location} and the temperature is {temperature}"

    return JsonResponse(
        {"client_ip": client_ip, "location": location, "greeting": greeting}
    )

from django.shortcuts import render
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os


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

    api_key = "c93e43f837557bf83551058e095c0fe5f32dc54adaf84895fcf2a821"

    try:
        response = requests.get(f"https://api.ipdata.co/{client_ip}?api-key={api_key}")
        data = response.json()
        location = data.get("city", "Unknown")
    except requests.exceptions.RequestException as e:
        location = "Unknown"

    temperature = "11 Degrees Celsius"
    greeting = f"Hello {visitor_name}, your location is {location} and the temperature is {temperature}"

    return JsonResponse(
        {"client_ip": client_ip, "location": location, "greeting": greeting}
    )
