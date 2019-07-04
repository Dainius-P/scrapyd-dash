from django.shortcuts import render
from .models import ScrapydServer, Task, ScrapydProject
from .operations.check_servers import update_servers
from .operations.projects_list import update_projects
from .operations.spiders_list import spiders_list
from .operations.tasks_cancel import cancel_task
from .operations.tasks_list import update_tasks
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from .forms import TaskForm
from django.views.generic import ListView, CreateView, UpdateView

from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import ServerSerializer, TaskSerializer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status

"""
List view for scrapyd servers
"""
class ServerList(APIView):

    """
    Retrieve all of the scrapyd servers
    """
    def get(self, request, format=None):
        update_servers()

        servers = ScrapydServer.objects.all()
        ser = ServerSerializer(servers, many=True)

        return JsonResponse(ser.data, safe=False)

    """
    Add new scrapyd server
    """
    def post(self, request, format=None):
        ser = ServerSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status=201, safe=False)

        return JsonResponse(ser.errors, status=400, safe=False)

"""
Details view for scrapyd servers
"""
class ServerDetails(APIView):

    """
    Remove scrapyd server from DB
    """
    def delete(self, request, pk, format=None):
        try:
            server = ScrapydServer.objects.get(pk=pk)
            server.delete()

            return JsonResponse({"deleted": True}, status=204)
        except ScrapydServer.DoesNotExist as e:
            return JsonResponse({"error": "Server does not exist"},
                                status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class TaskList(APIView):

    """
    Get list of all of the tasks
    """
    def get(self, request, format=None):
        update_tasks()

        tasks = Task.objects.all()
        ser = TaskSerializer(tasks, many=True)

        return JsonResponse(ser.data, safe=False)

    """
    Create new task
    """
    def post(self, request, format=None):
        ser = TaskSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data, status=201, safe=False)

        return JsonResponse(ser.errors, status=400, safe=False)

class TaskDetails(APIView):
    """
    Delete 
    """
    def delete(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk)

            """
            If the task is pending, it will be removed. 
            If the task is running, it will be terminated.
            """

            if task.status != "running":
                task.deleted = True
                task.save()

            r = cancel_task(
                task.server,
                task.project,
                task.id
            )

            return JsonResponse({"deleted": r}, status=204)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task does not exist"},
                                status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def index_view(request):
    update_servers()
    servers_list = ScrapydServer.objects.all()

    paginator = Paginator(servers_list, 10) # Show 10 servers per page
    page = request.GET.get('page')
    servers = paginator.get_page(page)

    return render(request, "servers.html", {"servers": servers})

"""
Delete scrapyd server
"""
def delete_server(request):
    if request.method == 'POST':
        data = request.POST

        try:
            ScrapydServer.objects.filter(ip=data.get('server_ip'),
                                         port=data.get('server_port')).delete()

            messages.success(request, 'Server {0}:{1} successfully\
                                       deleted'.format(data.get('server_ip'),
                                                       data.get('server_port')))

        except:
            messages.error(request, 'Something went wrong\
                                     adding server {0}:{1}'.format(data.get('server_ip'),
                                                                   data.get('server_port')))

    return HttpResponseRedirect(reverse('index'))

"""
Adds scrapyd server and checks the current status
"""
def add_server(request):
    if request.method == 'POST':
        data = request.POST

        try:
            ScrapydServer.objects.create(ip=data.get('server_ip'),
                                         port=data.get('server_port'))

            messages.success(request, 'Server {0}:{1} successfully\
                                       added'.format(data.get('server_ip'),
                                                     data.get('server_port')))

            update_servers()
            update_projects()
        except IntegrityError:
            messages.error(request, 'A server with this ip {0}:{1} \
                                     already exsists'.format(data.get('server_ip'),
                                                             data.get('server_port')))
        except:
            messages.error(request, 'Something went wrong\
                                     adding server {0}:{1}'.format(data.get('server_ip'),
                                                                   data.get('server_port')))

    return HttpResponseRedirect(reverse('index'))

def scheduled_tasks(request):
    return render(request, "scheduled_tasks.html", {"scheduled_tasks": []})

"""
List of tasks
"""
def tasks(request):
    update_tasks()
    tasks_list = Task.objects.all()

    paginator = Paginator(tasks_list, 10) # Show 10 tasks per page
    page = request.GET.get('page')
    tasks = paginator.get_page(page)

    return render(request, "tasks.html", {"tasks": tasks})


"""
Add new task
"""
class TaskCreateView(CreateView):
    model = Task
    fields = ("name", "project", "spider", "server")
    template_name = 'tasks_submit.html'
    success_url = reverse_lazy('tasks')

def add_task(request):
    if request.method == 'POST':
        data = request.POST
    else:
        return render(request, 'tasks_submit.html', {'form': {}})

    return HttpResponseRedirect(reverse('tasks'))


"""
Dynamic ajax load
"""
def load_projects(request):
    server_id = request.GET.get("server")
    if server_id:
        projects = ScrapydProject.objects.filter(server_id=server_id).order_by('name')
    else:
        projects = []

    return render(request,
                  "projects_dropdown_list_options.html",
                  {"projects": projects})

def load_spiders(request):
    project_id = request.GET.get("project")

    if project_id:
        project = ScrapydProject.objects.get(id=project_id)
        server_ip = "%s:%s" % (project.server.ip, project.server.port)
        spiders = spiders_list(server_ip, project.name)
    else:
        spiders = []

    return render(request,
                  "spiders_dropdown_list_options.html",
                  {"spiders": spiders})