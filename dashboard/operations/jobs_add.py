import requests

"""
Scheduls a task to run
"""
def add_job(project, spider, **kwargs):
	url = "http://{}/schedule.json".format(server)

	data = {
		"project": project,
		"spider": spider
	}

	data_merged = {**data, **kwargs}

	with requests.Session() as session:
		try:
			r = session.post(url, data=data_merged)
		except:
			return None

		return r.json()