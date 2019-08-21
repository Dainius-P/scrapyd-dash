from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from scrapyd_dash.operations import (check_servers,
							  		 projects_list,
							  		 tasks_list,
							  		 scheduled_tasks)


def start_updater():
    scheduler = BackgroundScheduler()

    scheduler.add_job(check_servers.update_servers, 'cron', second=0)
    scheduler.add_job(projects_list.update_projects, 'cron', second=30)
    scheduler.add_job(tasks_list.update_tasks, 'interval', seconds=10)

    scheduler.add_job(scheduled_tasks.check_scheduled, 'cron', second=10)

    
    scheduler.start()