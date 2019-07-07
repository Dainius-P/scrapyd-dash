import requests
import json

"""
Gets list of versions from a specific scrapyd server
and specific project

-server = ip:port
-project = project name
"""
def versions_list(server, project="default"):
	full_url = "http://{}:{}/listversions.json?project={}".format(server.ip,
																  server.port,
																  project)
	timeout = 5

	with requests.Session() as session:
		try:
			r = session.get(full_url, timeout=timeout)
		except:
			return None

		data = json.loads(r.text)

		return data.get("versions", [])
