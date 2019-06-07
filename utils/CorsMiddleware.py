class CorsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response['Access-Control-Allow-Origin'] = "https://grooving-frontend-d6.herokuapp.com"
        response['Access-Control-Allow-Methods'] = "GET,POST,PUT,OPTIONS,DELETE"
        response['Access-Control-Expose-Headers'] = 'x-auth'
        response['Access-Control-Allow-Headers'] = "Authorization,access-control-allow-origin, access-control-allow-headers, access-control-allow-methods, content-type, access-control-allow-credentials"
        response['Access-Control-Allow-Credentials'] = "true"
        return response
