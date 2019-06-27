from django.db.models import (
					   CharField,
					   DateTimeField,
					   PositiveIntegerField,
					   TimeField,
					   BooleanField,
					   Model)
from django.core.validators import MaxValueValidator


class ScrapydServer(Model):
	ip = CharField(max_length=128, primary_key=True)
	node_name = CharField(max_length=256)
	status = CharField(max_length=64)
	pending_tasks = PositiveIntegerField(default=0)
	finished_tasks = PositiveIntegerField(default=0)
	running_tasks = PositiveIntegerField(default=0)

	class Meta:
   		ordering = ['-ip']


class Task(Model):
	id = PositiveIntegerField(primary_key=True)
	name = CharField(max_length=256, null=False, blank=False)
	
	project = CharField(max_length=256, null=False)
	spider = CharField(max_length=256, null=False)
	status = PositiveIntegerField(null=False,
								  validators=[MaxValueValidator(3)])

	pages = PositiveIntegerField(null=True)
	items = PositiveIntegerField(null=True)
	pid = PositiveIntegerField(null=True)
	runtime = TimeField()
	start_datetime = DateTimeField(auto_now_add=True)
	finished_datetime = DateTimeField()

	log_href = CharField(max_length=1024, null=True)
	items_href = CharField(max_length=1024, null=True)

	create_datetime = DateTimeField(auto_now_add=True)
	update_datetime = DateTimeField(auto_now=True)

	deleted = BooleanField(null=False)

class ScheduledTasks(Model):
	id = PositiveIntegerField(primary_key=True)
	name = CharField(max_length=256, null=True)
	create_datetime = DateTimeField(auto_now_add=True)
	update_datetime = DateTimeField(auto_now=True)

	project = CharField(max_length=256, null=False)
	spider = CharField(max_length=256, null=False)

	year = PositiveIntegerField(null=False)
	month = PositiveIntegerField(null=False,
								 validators=[MaxValueValidator(12)])
	day = PositiveIntegerField(null=False,
							   validators=[MaxValueValidator(32)])
	week = PositiveIntegerField(null=False)
	day_of_week = PositiveIntegerField(null=False,
									   validators=[MaxValueValidator(7)])
	hour = PositiveIntegerField(null=False,
								validators=[MaxValueValidator(24)])
	minute = PositiveIntegerField(null=False,
								  validators=[MaxValueValidator(60)])
	second = PositiveIntegerField(null=False,
								  validators=[MaxValueValidator(60)])