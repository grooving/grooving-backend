import django


class CloseOldConnectionsMiddelware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        django.db.connections.close_all()
        return response
