from django.views import View

from api.models import Server


class BaseView(View):

    def get_server_public(self, request, server_id):
        return (Server.objects
            .filter(id=server_id)
            .with_character_count()
            .first())

    def get_server_private(self, request, server_id):
        return (Server.objects
            .filter(id=server_id)
            .filter(private_secret=request.GET.get('private_secret', None))
            .with_character_count()
            .first())
