#!/usr/bin/python

import json
import urllib
import urllib2
import time

# Sign up for a new app here
# http://www.strava.com/developers
# Aftewards, get Access Token from
# https://www.strava.com/settings/api
 
ACCESS_TOKEN = ''
 
page=0
per_page=200
num_activities=per_page
current_month = None

base_url = 'https://www.strava.com/api'
url = "/v3/activities/?access_token=" + ACCESS_TOKEN + "&per_page=" + str(per_page) + "&page=" + str(page)

file = open('strava.txt','w+')

file.write("Date : Distance : Pace : Duration : Ave HR : Max HR : Average Speed : Max Speed\n")

while num_activities == per_page:
	page=page+1
	url = "/v3/activities/?access_token=" + ACCESS_TOKEN + "&per_page=" + str(per_page) + "&page=" + str(page)
	req = urllib2.Request('%s%s' % (base_url, url), None)
	r = urllib2.urlopen(req)
	resp = json.loads(r.read())
	r.close()
	num_activities = len(resp)

	for activity in resp:
		distance = activity.get('distance')
		start_time = time.strptime(activity.get('start_date_local'), '%Y-%m-%dT%H:%M:%SZ')
		date = time.strftime('%a %m/%d/%y', start_time)

		month = time.strftime('%B', start_time)
		if month != current_month:
			current_month = month
			file.write('\n')
			file.write('--' + current_month + '--\n')
		

		avgheartrate = activity.get('average_heartrate')
		maxheartrate = activity.get('max_heartrate')
		avgspeed = '%.2f' % round(float(activity.get('average_speed') * 2.2369362920544),2)
		maxspeed = '%.2f' % round(float(activity.get('max_speed') * 2.2369362920544),2)
		# convert from km to mi and round
		miles = float(activity.get('distance')) * 0.000621371
		distance = '%.2f' % round(miles, 2)

		duration_seconds = activity.get('moving_time')

		pace = ''
		if miles > 0:
			seconds_per_mile = duration_seconds / miles
		else:
			seconds_per_mile = 0
		hours, remainder = divmod(seconds_per_mile, 3600)
		minutes, seconds = divmod(remainder, 60)
		pace = '(%.0f\'%02.0f/mi)' % (minutes, seconds)
		durhours, durrem = divmod(duration_seconds, 3600)
		durmins, dursecs = divmod(durrem,60)

		file.write(str(date) + " : " + distance.ljust(5) + "mi " + pace.ljust(11) + "" + str(durhours).rjust(2, '0') + ":" + str(durmins).rjust(2,'0') + ":" + str(dursecs).rjust(2, '0') + " " + str(avgheartrate).ljust(5) + " " + str(maxheartrate).ljust(5) + " " + avgspeed + " " + maxspeed + "\n")

file.close()
