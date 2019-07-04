from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from scrapyd_dash.operations import check_servers

def start_updater():
    scheduler = BackgroundScheduler()

    scheduler.add_job(check_servers.check_servers_status, 'interval', seconds=10)
    scheduler.start()