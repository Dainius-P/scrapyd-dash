from ..models import ScrapydServer
from concurrent.futures import ThreadPoolExecutor
import json
import requests
import asyncio


class CheckServers(object):
    """docstring for CheckServers"""
    def __init__(self):
        super(CheckServers, self).__init__()
        self.servers = ScrapydServer.objects.all() #scrapyd servers

    def check_server(self, session, server):
        url = "http://%s/daemonstatus.json" % server.ip

        with session.get(url) as response:
            data = response.json()

            server.node_name = data.get("node_name")
            server.status = data.get("status")
            server.pending_tasks = data.get("pending")
            server.finished_tasks = data.get("finished")
            server.running_tasks = data.get("running")

            server.save()

    async def execute_servers_check(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            with requests.Session() as session:
                # Initialize the event loop        
                loop = asyncio.get_event_loop()

                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.check_server, #function
                        *(session, server) # arguments
                    )
                    for server in self.servers
                ]

                for response in await asyncio.gather(*tasks):
                    pass

    def check_servers(self):
        loop = asyncio.new_event_loop();
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(self.execute_servers_check())
        loop.run_until_complete(future)