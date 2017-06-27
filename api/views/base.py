from django.views import View


class BasePublicView(View):

	def get_server(request, server_id):
		return (Server.objects
			.filter(id=server_id)
			.filter(
				Q(private_secret=request.GET.get('private_secret', None)) |
				Q(public_secret=request.GET.get('public_secret', None)))
			.first())


class BaseAdminView(View):

	def get_server(request, server_id):
		return (Server.objects
			.filter(id=server_id)
			.filter(public_secret=request.GET.get('public_secret', None))
			.first())