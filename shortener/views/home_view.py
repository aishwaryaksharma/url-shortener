from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from shortener.models import URLMapping

def home_view(request):
    if request.method == 'POST':
        original_url = request.POST.get('url')
        if not original_url:
            messages.error(request, 'Please enter a URL')
            return render(request, 'shortener/home.html')
        
        validate = URLValidator()
        try:
            validate(original_url)
        except ValidationError:
            messages.error(request, 'Invalid URL format')
            return render(request, 'shortener/home.html')
        
        mapping = URLMapping.objects.create(original_url=original_url)
        short_url = f"http://localhost:8000/{mapping.short_code}"
        return render(request, 'shortener/home.html', {
            'short_url': short_url,
            'original_url': original_url
        })
    
    return render(request, 'shortener/home.html')