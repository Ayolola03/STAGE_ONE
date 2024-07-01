from django.urls import path
from .views import web_server

urlpatterns = [
    path("api/web_server", web_server),
]
