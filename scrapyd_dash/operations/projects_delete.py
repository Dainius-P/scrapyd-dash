import requests

"""
Delete a project and all its uploaded versions.
"""
def delete_project(server, project):
	url = "http://{}/delproject.json".format(server)

	data = {
		"project": project
	}

	with requests.Session() as session:
		try:
			r = session.post(url, data=data)
		except:
			return None

		return r.json()
