from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from shortener.models import URLMapping
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def redirect_to_full_url(request, short_code):
    mapping = get_object_or_404(URLMapping, short_code=short_code)
    return redirect(mapping.original_url)