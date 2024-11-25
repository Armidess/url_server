from django.http import JsonResponse
from urllib.parse import urlparse

def process_url(request):
    url = request.GET.get('url')
    
    if not url:
        return JsonResponse({
            'error': 'URL parameter is required'
        }, status=400)
    
    try:
        # Basic URL validation
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError('Invalid URL')
        
        # Add your URL processing logic here
        result = {
            'url': url,
            'domain': parsed_url.netloc,
            'scheme': parsed_url.scheme,
            'path': parsed_url.path,
        }
        
        return JsonResponse(result)
    
    except ValueError as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'An error occurred while processing the URL'
        }, status=500)
