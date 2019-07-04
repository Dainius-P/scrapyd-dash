from rest_framework import serializers
from .models import ScrapydServer, Task
from .operations.projects_list import update_projects
from .operations.tasks_add import add_task

class ServerSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScrapydServer
		fields = (
			'ip',
			'port', 
			'node_name', 
			'status', 
			'status_message', 
			'pending_tasks',
			'finished_tasks',
			'running_tasks'
		)

		read_only_fields = (
			'node_name',
			'status',
			'status_message',
			'pending_tasks',
			'finished_tasks',
			'running_tasks'
		)

	def create(self, data):
		server = ScrapydServer(
			ip=data['ip'],
			port=data['port']
		)

		server.save()
		update_projects()

		return server

class TaskSerializer(serializers.ModelSerializer):
	project_name = serializers.CharField(source='project.name',
										 read_only=True)
	server_node = serializers.CharField(source='server.node_name',
										read_only=True)
	server_ip = serializers.CharField(source='server.ip',
									  read_only=True)
	server_port = serializers.CharField(source='server.port',
										read_only=True)

	class Meta:
		model = Task
		fields = (
			'id',
			'name',
			'project_name',
			'spider',
			'status',
			'server_node',
			'server_ip',
			'server_port',
			'pages',
			'items',
			'runtime',
			'start_datetime',
			'finished_datetime',
			'log_href'
		)

	def create(self, data):
		r = add_task(
			data['project'],
			data['spider'],
			data['server']
		)

		task = Task(
			name=data['name'],
			project=data['project'],
			spider=data['spider'],
			server=data['server'],
			id=r['jobid']
		)

		task.save()

		return task

