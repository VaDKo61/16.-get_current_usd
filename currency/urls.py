from django.urls import path
from .views import get_current_usd, redirect_to_usd

urlpatterns = [
    path('', redirect_to_usd),
    path('get-current-usd/', get_current_usd, name='get_current_usd'),
]
