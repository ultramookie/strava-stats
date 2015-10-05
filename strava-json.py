#!/usr/bin/env python

import json
import urllib
import urllib2
import time
import os.path
 
ACCESS_TOKEN = ''
 
page=0
per_page=200
jsondir = 'strava-json/'

num_activities=per_page

base_url = 'https://www.strava.com/api'
url = "/v3/activities/?access_token=" + ACCESS_TOKEN + "&per_page=" + str(per_page) + "&page=" + str(page)

while num_activities == per_page:
	page=page+1
	url = "/v3/activities/?access_token=" + ACCESS_TOKEN + "&per_page=" + str(per_page) + "&page=" + str(page)
	req = urllib2.Request('%s%s' % (base_url, url), None)
	r = urllib2.urlopen(req)
	resp = json.loads(r.read())
	r.close()
	num_activities = len(resp)

	for activity in resp:
		id = str(activity.get('id'))
		jsonfile = jsondir + id + ".json"
		if not os.path.isfile(jsonfile):
			file = open(jsonfile,'w+')
			json.dump(activity,file)
			file.close()
