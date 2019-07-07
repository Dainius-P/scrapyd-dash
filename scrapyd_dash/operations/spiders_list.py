import requests
import json

"""
Gets spiders list from specific scrapyd server and specific project

-server = ip:port
-project = project name
"""
def spiders_list(server, project="default"):
	full_url = "http://{}:{}/listspiders.json?project={}".format(server.ip,
																 server.port,
																 project)
	timeout = 5

	with requests.Session() as session:
		try:
			r = session.get(full_url, timeout=timeout)
		except:
			return None

		data = json.loads(r.text)

		return data.get("spiders", [])