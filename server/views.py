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
        f"https://api.ipdata.co/{client_ip}?api-key=c93e43f837557bf83551058e095c0fe5f32dc54adaf84895fcf2a821"
    )
    data = response.json()
    location = data.get("city", "Unknown")
    temperature = "11 Degress Celsuis"
    greeting = f"Hello {visitor_name}, your location is {location} and the temperature is {temperature}"

    return JsonResponse(
        {"client_ip": client_ip, "location": location, "greeting": greeting}
    )
