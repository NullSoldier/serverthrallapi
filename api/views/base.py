from django.views import View

from api.models import Server


class BaseView(View):

    def get_servers(self):
        return (Server.objects
            .with_character_count())

    def get_server_public(self, request, server_id):
        return (self.get_servers()
            .filter(id=server_id)
            .first())

    def get_server_private(self, request, server_id):
        return (self.get_servers()
            .filter(id=server_id)
            .filter(private_secret=request.GET.get('private_secret', None))
            .first())
