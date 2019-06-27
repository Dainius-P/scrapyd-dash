from django.conf import settings
from django.shortcuts import render
from .models import ScrapydServer
from django.core.paginator import Paginator

def index_view(request):
    servers_list = ScrapydServer.objects.all()

    paginator = Paginator(servers_list, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    servers = paginator.get_page(page)

    return render(request, "servers.html", {"servers": servers})
