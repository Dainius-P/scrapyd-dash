import requests

"""
Scheduls a task to run
"""
def add_task(project, spider, server, **kwargs):
	url = "http://{}:{}/schedule.json".format(server.ip, server.port)

	data = {
		"project": project.name,
		"spider": spider
	}

	data_merged = {**data, **kwargs}

	with requests.Session() as session:
		try:
			r = session.post(url, data=data_merged)
		except:
			return None

		return r.json()