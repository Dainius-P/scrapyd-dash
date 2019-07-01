import requests

"""
Cancel a spider run (aka. job). 
If the job is pending, it will be removed. 
If the job is running, it will be terminated.
"""
def cancel_job(server, project, job):
	url = "http://{}/cancel.json".format(server)

	data = {
		"project": project,
		"job": job
	}

	with requests.Session() as session:
		try:
			r = session.post(url, data=data)
		except:
			return None

		return r.json()