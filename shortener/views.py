from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from .models import URLMapping

class ShortenURLView(APIView):
    def post(self, request):
        original_url = request.data.get('url')
        mapping = URLMapping.objects.create(original_url=original_url)
        return Response({
            "short_url": f"http://localhost:8000/{mapping.short_code}"
        }, status=status.HTTP_201_CREATED)

def redirect_to_full_url(request, short_code):
    mapping = get_object_or_404(URLMapping, short_code=short_code)
    return redirect(mapping.original_url)