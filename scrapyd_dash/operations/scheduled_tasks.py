from ..models import ScheduledTask, Task
from .tasks_add import add_task
from datetime import timedelta, datetime

def generate_first_run(s_task, now):
    if s_task.hour and s_task.hour != now.hour:
        return 0
    elif s_task.minute and s_task.minute != now.minute:
        return 0
    elif s_task.day_of_week and s_task.day_of_week != int(now.strftime('%w')):
        return 0
    elif s_task.week and s_task.week != int(now.strftime('%U')):
        return 0
    elif s_task.day and s_task.day != now.day:
        return 0
    elif s_task.month and s_task.month != now.month:
        return 0
    elif s_task.year and s_task.year != now.year:
        return 0

"""
Check scheduled tasks
"""

def check_scheduled():
    s_tasks = ScheduledTask.objects.all()
    now = datetime.now()
    print(now)

    for s_task in s_tasks:
        if not s_task.next_run and not generate_first_run:
            continue

        if s_task.next_run and now.replace(microsecond=0, second=0) != s_task.next_run:
            continue

        task_resp = add_task(s_task.project,
                             s_task.spider,
                             s_task.server)

        s_task.last_run = now

        """
        if day of week is picked
        """
        if s_task.day_of_week:
            day = now.day + 7
        else:
            day = now.day

        s_task.next_run = datetime(now.year + 1 if s_task.month else now.year,
                                   now.month + 1 if s_task.day else now.month,
                                   now.day + 1 if s_task.hour else day,
                                   now.hour + 1 if s_task.minute else now.hour,
                                   now.minute,
                                   0)


        s_task.save()
        
        task = Task.objects.create(
            id=task_resp.get("jobid"),
            name="scheduled_%s" % (s_task.name),
            project=s_task.project,
            spider=s_task.spider,
            server=s_task.server
        )

        s_task.tasks.add(task)
        s_task.save()