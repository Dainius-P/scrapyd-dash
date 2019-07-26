import requests
import json

"""
Gets more detailed logs
"""
def get_log(href):
	timeout = 5
	try:
		with requests.get(href, timeout=timeout) as r:
			return r.json()
	except:
		raise Exception("LogParser server does not respond") 