import requests
import json

"""
Gets list of jobs that are running/pending/finished
from a specific scrapyd server and project

-server = ip:port
-project = project name
"""
def jobs_list(server, project="default"):
	full_url = "http://{}/listjobs.json?project={}".format(server, project)
	timeout = 5
	jobs = []
	status = ["finished", "pending", "running"]

	with requests.Session() as session:
		try:
			r = session.get(full_url, timeout=timeout)
		except:
			return None

		data = json.loads(r.text)

		for s in status:
			jobs.append(
				{
					"status": s,
					"jobs": data.get(s, [])
				}
			)

		return jobs