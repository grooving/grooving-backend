from django.http import HttpResponseForbidden


class Erro500Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 600 > response.status_code >= 500:
            return HttpResponseForbidden()
        return response
