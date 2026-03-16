from django.urls import path
from .views import ShortenURLView, redirect_to_full_url, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('api/shorten/', ShortenURLView.as_view(), name='shorten'),
    path('<str:short_code>/', redirect_to_full_url, name='redirect'),
]
