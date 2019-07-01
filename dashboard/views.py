from django.shortcuts import render
from .models import ScrapydServer
from .operations.check_servers import CheckServers
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

def index_view(request):
    servers_list = ScrapydServer.objects.all()

    paginator = Paginator(servers_list, 10) # Show 25 servers per page
    page = request.GET.get('page')
    servers = paginator.get_page(page)

    return render(request, "servers.html", {"servers": servers})

def delete_server(request):
	if request.method == 'POST':
		data = request.POST

		try:
			ScrapydServer.objects.filter(ip=data.get('server_ip'),
									 	 port=data.get('server_port')).delete()

		except:
			pass

	return HttpResponseRedirect(reverse('index'))


def add_server(request):
	if request.method == 'POST':
		data = request.POST

		try:
			ScrapydServer.objects.create(ip=data.get('server_ip'),
										 port=data.get('server_port'))

			c = CheckServers()
			c.check_servers()

			messages.success(request, 'Server {0}:{1} successfully\
									   added'.format(data.get('server_ip'),
													 data.get('server_port')))

		except Exception as e:
			print(e)

	return HttpResponseRedirect(reverse('index'))
