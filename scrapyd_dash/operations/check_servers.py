from ..models import ScrapydServer
from concurrent.futures import ThreadPoolExecutor
import json
import requests
import asyncio

"""
Check scrapyd servers status, tasks running/pending/finished etc.
and saves the data to the database
"""
def update_servers():
    """
    Gets server list from the database
    """
    servers = ScrapydServer.objects.all()

    """
    Creates events for each server
    """
    loop = asyncio.new_event_loop();
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(check_servers(servers))
    loop.run_until_complete(future)

def check_server(session, server):
    url = "http://{}:{}/daemonstatus.json".format(server.ip, server.port)

    try:
        with session.get(url, timeout=2) as response:
            data = response.json()

            server.node_name = data.get("node_name")
            server.status = data.get("status")
            server.pending_tasks = data.get("pending")
            server.running_tasks = data.get("running")
            server.finished_tasks = data.get("finished")

            server.save()

    except Exception as e:
        server.status = "error"
        server.status_message = e

        server.save()

async def check_servers(servers):
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as session:
            # Initialize the event loop        
            loop = asyncio.get_event_loop()

            tasks = [
                loop.run_in_executor(
                    executor,
                    check_server, #function
                    *(session, server) # arguments
                )
                for server in servers
            ]

            for response in await asyncio.gather(*tasks):
                pass