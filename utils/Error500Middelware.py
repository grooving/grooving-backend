from django.http import HttpResponseForbidden

from django.http import JsonResponse
class Erro500Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 600 > response.status_code >= 500:
            response = JsonResponse({'error': 'error'})
            response.status_code = 400

        return response
