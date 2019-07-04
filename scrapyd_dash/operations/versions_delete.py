import requests

"""
Delete a project version. 
If there are no more versions available for a given project, that project will be deleted too.
"""
def delete_version(server, project, version):
	url = "http://{}/delversion.json".format(server)

	data = {
		"project": project,
		"version": version
	}

	with requests.Session() as session:
		try:
			r = session.post(url, data=data)
		except:
			return None

		return r.json()
