# python-solar-incidentangle

<img src="plots/solar-incidentangle-2.png" width="800" height="600"/>

<h1>Solar Incident Angle Calculator</h1>
<p>
A python-based calculator for determing the incident angle of a solar panel at a specified latitude/longitude, elevation, tilt angle and azimuth angle.
</p>

<p>
To run a calculation, first edit the following input parameters...
</p>

<pre>
<code>
p_latitude_dd = 45.523097;
p_longitude_dd = -122.681325;
p_tilt_deg = 45.0;
p_azimuth_deg = 0.0;
p_elevation_m = 17.0;
p_interval_minutes = 10;

p_start = "2017-01-01T00:00";
p_end = "2018-01-01T00:00";

p_zenith_filter = False;
p_zenith_limit = 100;
</code>
</pre>

Based on the following references...

Solar Position Code
<a href="https://github.com/s-bear/sun-position">https://github.com/s-bear/sun-position</a>

Solar Position Theory
<a href="http://www.me.umn.edu/courses/me4131/LabManual/AppDSolarRadiation.pdf">http://www.me.umn.edu/courses/me4131/LabManual/AppDSolarRadiation.pdf/</a>
