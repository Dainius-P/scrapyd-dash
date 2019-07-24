from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from scrapyd_dash.operations import check_servers
from scrapyd_dash.operations import projects_list
from scrapyd_dash.operations import tasks_list

def start_updater():
    scheduler = BackgroundScheduler()

    scheduler.add_job(check_servers.update_servers, 'cron', second=0)
    scheduler.add_job(projects_list.update_projects, 'cron', second=30)
    scheduler.add_job(tasks_list.update_tasks, 'interval', seconds=5)

    
    scheduler.start()