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
    miles = float(activity.get('distance')) * 0.000621371
    feet = float(activity.get('total_elevation_gain')) * 3.28084
    avg_mph = float(activity.get('average_speed')) * 2.23694
    avg_pace = 60 / avg_mph
    max_mph = float(activity.get('max_speed')) * 2.23694
    max_pace = 60 / avg_mph
    activity['distance_mileage'] = miles
    activity['total_elevation_gain_feet'] = feet
    activity['average_speed_mph'] = avg_mph
    activity['average_pace'] = avg_pace
    activity['max_speed_mph'] = max_mph
    activity['max_pace'] = max_pace
    if activity.get('average_temp'):
      avg_f = (float(activity.get('average_temp')) * 1.8) + 32
      activity['average_temp_f'] = avg_f
    if activity.get('start_latlng'):
      start_list = activity.get('start_latlng')
      start_latlng = '{"lat": ' + str(start_list[0]) + "," + '"lon": ' + str(start_list[1]) + '}'
      start_json = json.loads(start_latlng)
      activity['start_latlng'] = start_json
    if activity.get('end_latlng'):
      end_list = activity.get('end_latlng')
      end_latlng = '{"lat": ' + str(end_list[0]) + "," + '"lon": ' + str(end_list[1]) + '}'
      end_json = json.loads(end_latlng)
      activity['end_latlng'] = end_json
    es.index(index=index, doc_type="activity", id=id, body=activity)
