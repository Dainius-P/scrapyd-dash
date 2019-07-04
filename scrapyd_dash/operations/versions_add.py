import requests

"""
Add a version to a specific scrapyd server

-server = ip:port
-project = project name
-version = version name
-egg = egg name
"""
def add_version(server, project, version, egg):
	url = "http://{}/addversion.json".format(server)

	data = {
		"project": project,
		"version": version,
		"egg": egg
	}

	with requests.Session() as session:
		try:
			r = session.post(url, data=data)
		except:
			return None

		return r.json()
