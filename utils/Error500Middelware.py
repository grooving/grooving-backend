from django.http import HttpResponseForbidden


class Erro500Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 600 > response.status_code >= 500:
            response["Content-Type"] = "application/json"
            response.status_code = 401
            response.content= "{ \"error\":\"error!\""+"}"

            response.status_code = 401
            response['result'] = 'error'
            response['message'] = 'Some error message'
        return response
