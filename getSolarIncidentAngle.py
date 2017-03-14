#!/usr/bin/python

from sunposition import sunpos
import datetime
import math
import matplotlib.pyplot as plt
import csv

############
# REFERENCES
# Solar Position Code...https://github.com/s-bear/sun-position
# Solar Position Concepts...http://www.me.umn.edu/courses/me4131/LabManual/AppDSolarRadiation.pdf
# Data Validation...https://www.nrel.gov/midc/solpos/solpos.html

########
# INPUTS 

p_latitude_dd = 45.523097
p_longitude_dd = -122.681325
p_tilt_deg = 45.0
p_azimuth_deg = 0.0
p_elevation_m = 17.0
p_interval_minutes = 10

p_start = '2017-01-01T00:00'
p_end = '2018-01-01T00:00'

p_zenith_filter = False
p_zenith_limit = 100

###########
# FUNCTIONS

# FUNCTION: convert degrees to radians
def deg2rad(deg):
	rad = deg / 180.0 * math.pi;
	return rad
	
# FUNCTION: convert radians to degrees
def rad2deg(rad):
	deg = rad / math.pi * 180.0;
	return deg
	
# FUNCTION: get solar position data
def getSolarPosition(t, project_data):

	# Get solar position from lat/lng, elevation and datetime
	phi, theta_h, rasc, d, h = sunpos(t, project_data['latitude'], project_data['longitude'], project_data['elevation'])[:5]
	
	# Convert azimuth (N) to azimuth (S)
	phi_south = phi - 180.0;
	
	# Calculate tilt angle from vertical
	eta = project_data['tilt'];
	
	# Calculate surface-solar azimuth angle
	gamma = math.fabs((phi_south - project_data['azimuth']));
	
	if project_data['zenith_filter'] and theta_h > project_data['zenith_limit']:
		theta_h = project_data['zenith_limit']

	# Calculate altitude angle
	beta = 90.0 - theta_h;
	
	# Calculate incident angle to surface
	theta = rad2deg(math.acos((( math.cos(deg2rad(beta)) * math.cos(deg2rad(gamma)) * math.sin(deg2rad(eta)) ) + (math.sin(deg2rad(beta)) * math.cos(deg2rad(eta))))));
	
	# Solar position datum
	sp_datum = {
		'Datetime_UTC': t,
		'Azimuth': phi,
		'Zenith': theta_h,
		'RightAscension': rasc,
		'Declination': d,
		'HourAngle': h,
		'IncidentAngle': theta
	}
	
	return sp_datum
		
# FUNCTION: loop through timestamp array, calculate solar position
def loopSolarPositionByProject(project_data):

	# Convert start/end timestamps to datetime
	start_f = datetime.datetime.strptime(p_start, "%Y-%m-%dT%H:%M")
	end_f = datetime.datetime.strptime(p_end, "%Y-%m-%dT%H:%M")

	# Solar position data array
	sp_data = []
	
	# Set start timestamp
	dt = start_f
	
	# Set timestamp invertal
	delta = datetime.timedelta(minutes=project_data['interval'])

	# Loop through timestamps...
	while dt <= end_f:

		# Print timestamp
		#print dt.strftime("%Y-%m-%dT%H:%M")
		
		sp_datum = getSolarPosition(dt, project_data)
		
		# Add solar position datum to data array
		sp_data.append(sp_datum);
		
		# Increment timestamp by +1 delta
		dt += delta
		
	return sp_data
	
# FUNCTION: export data to CSV
def export2CSV(data, filename):

	with open(filename, 'wb') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Timestamp_UTC','Zenith','Azimuth','IncidentAngle'])
		for ii in range(1,len(data)):
			datum = data[ii]
			writer.writerow([datum['Datetime_UTC'], datum['Zenith'], datum['Azimuth'],datum['IncidentAngle']])

#####
# RUN

# Create project data object
project_data = {
	'latitude': p_latitude_dd,
	'longitude': p_longitude_dd,
	'elevation': p_elevation_m,
	'tilt': p_tilt_deg,
	'azimuth': p_azimuth_deg,
	'zenith_limit': p_zenith_limit,
	'zenith_filter': p_zenith_filter,
	'start': p_start,
	'end': p_end,
	'interval': p_interval_minutes
}

# Create solar position data array + insert into PADRE
print project_data
print 'Looping through solar position calcs...'
sp_data = loopSolarPositionByProject(project_data);
print 'Done!'

#############
# OUTPUT DATA

o_datetime_utc = [x['Datetime_UTC'] for x in sp_data]		
o_azimuth = [x['Azimuth'] for x in sp_data]		
o_zenith = [x['Zenith'] for x in sp_data]		
o_incident_angle = [x['IncidentAngle'] for x in sp_data]

#############
# EXPORT DATA
#export2CSV(sp_data, 'data.csv')
	
###########
# PLOT DATA

title = 'Solar Incident Angle @ (' + str(p_latitude_dd) + ',' + str(p_longitude_dd) + ')'
title += '\nTilt (Horizontal): ' + str(p_tilt_deg) + ' deg, Azimuth (South CC): ' + str(p_azimuth_deg) + ' deg @ Elevation: ' + str(p_elevation_m) + ' m'
title += '\n' + p_start + ' to ' + p_end + ' @ ' + str(p_interval_minutes) + ' min Interval'

plt.close('all')
f, ax = plt.subplots()
ax.plot(o_datetime_utc, o_azimuth, 'b')
ax.plot(o_datetime_utc, o_zenith, 'g')
ax.plot(o_datetime_utc, o_incident_angle, 'r')
ax.set_title(title)
plt.tight_layout()
f.savefig('plots/solar-incidentangle-1.png')   # save the figure to file
plt.close(f)

# Three subplots sharing both x/y axes
f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
ax1.plot(o_datetime_utc, o_azimuth, 'b')
ax2.plot(o_datetime_utc, o_zenith, 'g')
ax3.plot(o_datetime_utc, o_incident_angle, 'r')
# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
f.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
ax1.set_title(title)
ax1.set_ylabel('Azimuth (South CC) [deg]',fontsize=9)
ax2.set_ylabel('Zenith (Vertical) [deg]',fontsize=9)
ax3.set_ylabel('Incident Angle [deg]',fontsize=9)
plt.tight_layout()
f.savefig('plots/solar-incidentangle-2.png')   # save the figure to file
plt.close(f)
