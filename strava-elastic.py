#!/usr/bin/env python

import json
import urllib
import urllib2
import time
from elasticsearch import Elasticsearch
 
ACCESS_TOKEN = ''

elastichost='localhost:9200'
page=0
per_page=200
num_activities=per_page

base_url = 'https://www.strava.com/api'
url = "/v3/activities/?access_token=" + ACCESS_TOKEN + "&per_page=" + str(per_page) + "&page=" + str(page)

es = Elasticsearch(elastichost)

while num_activities == per_page:
	page=page+1
	url = "/v3/activities/?access_token=" + ACCESS_TOKEN + "&per_page=" + str(per_page) + "&page=" + str(page)
	req = urllib2.Request('%s%s' % (base_url, url), None)
	r = urllib2.urlopen(req)
	resp = json.loads(r.read())
	r.close()
	num_activities = len(resp)

	for activity in resp:
		id = activity.get('id')
		start_time = time.strptime(activity.get('start_date_local'), '%Y-%m-%dT%H:%M:%SZ')
		month = time.strftime('%m', start_time)
		year = time.strftime('%Y', start_time)
		index = 'strava-' + year + '-' + month
		es.index(index=index, doc_type="activity", id=id, body=activity)
