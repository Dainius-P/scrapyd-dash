import requests
import json

"""
Gets list of projects inside a specific scrapyd server

-server = ip:port
"""
def projects_list(server):
	full_url = "http://{}/listprojects.json".format(server)
	timeout = 5

	with requests.Session() as session:
		try:
			r = session.get(full_url, timeout=timeout)
		except:
			return None

		data = json.loads(r.text)

		return data.get("projects", [])

