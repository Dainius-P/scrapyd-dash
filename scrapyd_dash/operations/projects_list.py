from concurrent.futures import ThreadPoolExecutor
from ..models import ScrapydServer, ScrapydProject
import json
import requests
import asyncio

"""
Gets list of projects inside a specific scrapyd server

-server = ip:port
"""
def projects_list(session, server):
    full_url = "http://{}:{}/listprojects.json".format(server.ip,
                                                       server.port)
    timeout = 5

    try:
        with session.get(full_url, timeout=timeout) as response:
            data = json.loads(response.text)

            for project in data.get("projects", []):
                ScrapydProject.objects.update_or_create(
                    server=server,
                    name=project
                )
    except:
        pass

async def check_projects(servers):
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            # Initialize the event loop        
            loop = asyncio.get_event_loop()

            tasks = [
                loop.run_in_executor(
                    executor,
                    projects_list, #function
                    *(session, server) # arguments
                )
                for server in servers
            ]

            for response in await asyncio.gather(*tasks):
                pass

def update_projects():
    servers = ScrapydServer.objects.filter(status="ok")

    """
    Creates events for each server
    """
    loop = asyncio.new_event_loop();
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(check_projects(servers))
    loop.run_until_complete(future)