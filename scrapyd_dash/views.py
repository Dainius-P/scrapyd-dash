from django.shortcuts import render
from django.core.paginator import Paginator
from .models import ScrapydServer, Task, ScrapydProject, ScrapydProjectVersion, ScheduledTasks
from .operations.projects_list import update_projects
from .operations.spiders_list import spiders_list
from .operations.tasks_cancel import cancel_task
from .operations.get_log import get_log
from .operations.tasks_add import add_task
from .operations.check_servers import update_servers
from .operations.tasks_list import update_tasks
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.views import View
from .serializers import *
from django.contrib.auth import authenticate, login, logout

class ServersListView(View):
    template_view = "servers.html"

    """
    This dispatcher is here because django does not 
    support delete method
    """
    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(ServersListView, self).dispatch(*args, **kwargs)

    """
    Retrieve list of scrapyd servers
    """
    def get(self, request, *args, **kwargs):
        servers_list = ScrapydServer.objects.all()
        pagi = Paginator(servers_list, 10) # Show 10 servers

        page = request.GET.get('page')
        servers = pagi.get_page(page)

        return render(request,
                      self.template_view,
                      {"servers": servers})

    """
    Add scrapyd server
    """
    def post(self, request, *args, **kwargs):
        data = request.POST

        server_ip = data.get('server_ip')
        server_port = data.get('server_port')

        try:
            ScrapydServer.objects.create(
                ip=server_ip,
                port=server_port
            )

            update_servers()
            update_projects()

            message = "Server {}:{} successfully added".format(
                server_ip,
                server_port
            )

            messages.success(request, message)

        except IntegrityError as e:
            message = "A server with this ip {}:{} already exist".format(
                server_ip,
                server_port
            )
            messages.error(request, message)
        except:
            message = """Something went wrong adding server {}:{}""".format(
                server_ip,
                server_port
            )

            messages.error(request, message)

        return HttpResponseRedirect(reverse('servers'))

    """
    Delete scrapyd server
    """
    def delete(self, request, *args, **kwargs):
        data = request.POST

        server_ip = data.get('server_ip')
        server_port = data.get('server_port')

        try:
            ScrapydServer.objects.filter(
                ip=server_ip,
                port=server_port
            ).delete()

            message = "Successfully deleted server {}:{}".format(
                server_ip,
                server_port
            )

            messages.success(request, message)
        except:
            message = "Something went wrong deleting server {}:{}".format(
                server_ip,
                server_port
            )

            messages.error(request, message)

        return HttpResponseRedirect(reverse('servers'))

"""
View dedicated for showing tasks in a table and creating new tasks
"""
class TasksListView(View):
    template_view = "tasks.html"

    """
    Revtrieves list of tasks
    """
    def get(self, request, *args, **kwargs):
        tasks_list = Task.objects.filter(deleted=False)
        pagi = Paginator(tasks_list, 10) # Show 10 tasks

        page = request.GET.get('page')
        tasks = pagi.get_page(page)

        servers = ScrapydServer.objects.filter(status="ok")

        return render(request,
                      self.template_view,
                      {"tasks": tasks,
                       "servers": servers})

    """
    Add a new task
    """
    def post(self, request, *args, **kwargs):
        data = request.POST

        task_name = data.get('name')
        server_pk = data.get('server')
        project_pk = data.get('project')
        version_pk = data.get('version')
        spider_name = data.get('spider')

        server = ScrapydServer.objects.get(pk=server_pk)
        project = ScrapydProject.objects.get(pk=project_pk)

        if version_pk:
            version = ScrapydProjectVersion.objects.get(pk=version_pk)
        else:
            version = None

        task_resp = add_task(project, spider_name, server, version)

        try:
            Task.objects.create(
                id=task_resp.get("jobid"),
                name=task_name,
                project=project,
                spider=spider_name,
                server=server
            )
            message = "Successfully created task: {}".format(task_resp.get("jobid"))

            messages.success(request, message)
        except:
            message = "Something went wrong creating new task"
            messages.error(request, message)

        return HttpResponseRedirect(reverse('tasks'))

def get_projects(request):
    if request.method == 'GET':
        server = request.GET.get('server')
        projects = ScrapydProject.objects.filter(server=server)

        ser = ScrapyProjectSerializer(projects, many=True)

        return JsonResponse(ser.data, safe=False)

def get_versions(request):
    if request.method == 'GET':
        project = request.GET.get('project')

        versions = ScrapydProjectVersion.objects.filter(project=project)

        ser = ScrapyProjectVersionSerializer(versions, many=True)

        return JsonResponse(ser.data, safe=False)

def get_spiders(request):
    if request.method == 'GET':
        project_pk = request.GET.get('project')
        server_pk = request.GET.get('server')
        version_pk = request.GET.get('version')

        server = ScrapydServer.objects.get(pk=server_pk)
        project = ScrapydProject.objects.get(pk=project_pk)

        spiders = spiders_list(server, project)

        return JsonResponse(spiders, safe=False)

"""
View for logging in
"""
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            message = "Hello %s. You Successfully logged in" % (username)
            messages.success(request, message)

        else:
            message = "Invalid login"
            messages.error(request, message)

    return HttpResponseRedirect(reverse('servers'))

"""
View for logging out
"""
def logout_view(request):
    if request.user.is_authenticated:
        try:
            logout(request)
            message = "You Successfully logged out"
            messages.success(request, message)
        except:
            message = "Something went wrong"
            messages.error(request, message)

    return HttpResponseRedirect(reverse('servers'))


"""
View dedicated for task details
"""
class TaskDetailsView(View):
    template_view = "task_details.html"

    """
    This dispatcher is here because django does not 
    support delete method
    """
    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(TaskDetailsView, self).dispatch(*args, **kwargs)

    """
    Get task details
    """
    def get(self, request, pk, *args, **kwargs):

        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            message = "Task with id: {} does not exist".format(pk)
            messages.error(request, message)

            return HttpResponseRedirect(reverse('tasks'))

        try:
            log = get_log(task.log_href)
        except Exception as e:
            messages.error(request, e)

            return HttpResponseRedirect(reverse('tasks'))


        return render(request,
                      self.template_view,
                      {"task": task,
                       "log": log})
    """
    Deletes task
    If the task is pending/finished, it will be removed. 
    If the task is running, it will be terminated.
    """
    def delete(self, request, pk, *args, **kwargs):
        data = request.POST

        try:
            task = Task.objects.get(id=pk)

            if task.status == "finished":
                task.deleted = True
                task.save()

                message = "Successfully deleted task: {}".format(pk)
            else:
                cancel_task(task.server, task.project, pk)

                message = "Stopping task: {}".format(pk)

            messages.success(request, message)
        except Task.DoesNotExist:
            message = "Task {} does not exist".format(pk)

            messages.error(request, message)

        except:
            message = "Something went wrong \
                       deleting/terminating task: {}".format(pk)

            messages.error(request, message)

        return HttpResponseRedirect(reverse('tasks'))