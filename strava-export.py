#!/usr/local/bin/python

import json
import urllib
import urllib2
import time
 
ACCESS_TOKEN = ''
 
page=0
per_page=200
num_activities=per_page
current_month = None
current_month_mileage = 0
all_time_mileage = 0
all_time_seconds = 0

base_url = 'https://www.strava.com/api'
url = "/v3/activities/?access_token=" + ACCESS_TOKEN + "&per_page=" + str(per_page) + "&page=" + str(page)

file = open('/home/public/strava.txt','w+')

file.write("Date : Distance : Pace : Duration : Avg HR : Max HR : Avg Speed : Max Speed : Avg Cadence : Elevation Gain\n")

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
		type = activity.get('type')
		if type == 'Run':
			start_time = time.strptime(activity.get('start_date_local'), '%Y-%m-%dT%H:%M:%SZ')
			date = time.strftime('%a %m/%d/%y', start_time)

			month = time.strftime('%B', start_time)
			if month != current_month:
				current_month = month
				file.write('\n')
				if current_month_mileage > 0:
					file.write('Total Distance: ' + current_month_distance + ' miles\n')
					file.write('\n')
					current_month_mileage = 0
				file.write('--' + current_month + '--\n')
		
			elevationgain = activity.get('total_elevation_gain')		
			avgcadence = activity.get('average_cadence')
			avgheartrate = activity.get('average_heartrate')
			maxheartrate = activity.get('max_heartrate')
			avgspeed = '%.2f' % round(float(activity.get('average_speed') * 2.2369362920544),2)
			maxspeed = '%.2f' % round(float(activity.get('max_speed') * 2.2369362920544),2)
			# convert from km to mi and round
			miles = float(activity.get('distance')) * 0.000621371
			current_month_mileage = current_month_mileage + miles
			all_time_mileage = all_time_mileage + miles
			all_time_distance = '%.2f' % round(all_time_mileage, 2)
			current_month_distance = '%.2f' % round(current_month_mileage, 2)
			distance = '%.2f' % round(miles, 2)

			duration_seconds = activity.get('moving_time')
			all_time_seconds = all_time_seconds + duration_seconds

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

			file.write(str(date) + " : " + distance.ljust(5) + "mi " + pace.ljust(11) + "" + str(durhours).rjust(2, '0') + ":" + str(durmins).rjust(2,'0') + ":" + str(dursecs).rjust(2, '0') + " " + str(avgheartrate).ljust(5) + " " + str(maxheartrate).ljust(5) + " " + avgspeed.ljust(5) + " " + maxspeed.ljust(5) + " " + str(avgcadence).ljust(6) + " " + str(elevationgain).ljust(6) + "\n")


pace = ''
if miles > 0:
	seconds_per_mile = all_time_seconds / all_time_mileage
else:
	seconds_per_mile = 0
hours, remainder = divmod(seconds_per_mile, 3600)
minutes, seconds = divmod(remainder, 60)
pace = '(%.0f\'%02.0f/mi)' % (minutes, seconds)
durhours, durrem = divmod(all_time_seconds, 3600)
durmins, dursecs = divmod(durrem,60)

file.write('\n')
file.write('Total Distance: ' + current_month_distance + ' miles\n')
file.write('\n')
file.write('----------------\n')
file.write('All Time Metrics\n')
file.write('----------------\n')
file.write('Distance: ' + all_time_distance + ' miles\n')
file.write('Pace: ' + pace + '\n')
file.write('Duration: ' + str(durhours) + ":" + str(durmins) + ":" + str(dursecs) + '\n')
file.write('----------------\n')
file.close()
