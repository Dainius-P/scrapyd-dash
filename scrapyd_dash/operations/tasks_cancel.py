import requests

"""
Cancel a spider run (aka. task). 
If the task is pending, it will be removed. 
If the task is running, it will be terminated.
"""
def cancel_task(server, project, task_id):
	url = "http://{}:{}/cancel.json".format(server.ip,
											server.port)

	data = {
		"project": project.name,
		"job": task_id
	}

	with requests.Session() as session:
		try:
			r = session.post(url, data=data)
		except:
			return None

		return r.json()