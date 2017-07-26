from django.views import View

from api.models import Server


class BasePublicView(View):

    def get_server(self, request, server_id):
        return (Server.objects
            .filter(id=server_id)
            .first())


class BaseAdminView(View):

    def get_server(self, request, server_id):
        return (Server.objects
            .filter(id=server_id)
            .filter(private_secret=request.GET.get('private_secret', None))
            .first())
