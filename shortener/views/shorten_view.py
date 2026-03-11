from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from shortener.models import URLMapping
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class ShortenURLView(APIView):
    def post(self, request):
        original_url = request.data.get('url')
        validate = URLValidator()
        try:
            validate(original_url)
        except ValidationError:
            return Response({"error": "Invalid URL format"}, status=400)

        mapping = URLMapping.objects.create(original_url=original_url)
        return Response({
            "short_url": f"http://localhost:8000/{mapping.short_code}"
        }, status=status.HTTP_201_CREATED)

