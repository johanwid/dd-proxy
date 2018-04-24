
if (1): 
	"""
	Website availability & performance monitoring

	The problem / assignment

	OVERVIEW

	- Create a console program to monitor performance and 
	  availability of websites
	- Websites and check intervals are user defined
	- Users can keep the console app running and monitor the websites

	STATS

	-  Check the different websites with their corresponding check intervals
	   -  Compute a few interesting metrics: availability, max/avg 
	   	  response times, response codes count and more...
	   -  Over different timeframes: 2 minutes and 10 minutes
	-  Every 10s, display the stats for the past 10 minutes for each website
	-  Every minute, displays the stats for the past hour for each website

	ALERTING

	-  When a website availability is below 80% for the past 2 minutes, 
	   add a message saying that 
	   "Website {website} is down. availability={availablility}, time={time}"
	-  When availability resumes for the past 2 minutes, add another 
	   message detailing when the alert recovered
	-  Make sure all messages showing when alerting thresholds are crossed 
	   remain visible on the page for historical reasons

	TESTS & QUESTIONS

	- Write a test for the alerting logic
	- Explain how you'd improve on this application design

	http://www.imdb.com

	"""
	pass

import urllib2 as ul
import time
import threading as th
import multiprocessing as mp



"""
output dashboard, include interesting parts of information
add parallelization for multiple websites
run an outer while loop that does the 10 minute check in the background

interesting things:
how long site is down
average time of outage
average time between outages

deliverables:
availability
max/avg response times
response codes count

note: interval may return empty if website never up or dne
"""



def get_stats(url, timespan):
	
	begin = time.time()			# begging time for entire function
	codes = dict()				# http code mapped to total occurrences
	times = dict()				# http code mapped to sum of req durations
	times_list = list()			# request durations
	all_intervals = list()		# up and down times
	isDown = False;				# flag to modify time if site is down
	speed = None;				# in case website is never up / dne
	LW = 2						# multiplier for urlopen timeout
	interval = 0				# initialize time interval of site being up

	duration = time.time() + timespan
	# duration = time.time() + 30		
	while (time.time() < duration):
		try:
			if (len(times_list) != 0):
				TO = max(times_list)
				start = time.time()
				ul.urlopen(url, timeout = TO * LW)
				speed = time.time() - start
				times_list.append(speed)
			else:
				start = time.time()
				url_open = ul.urlopen(url)
				url_open
				speed = time.time() - start
				times_list.append(speed)
			code = url_open.getcode()
			interval += speed
			isDown = False
		except IOError:
			code = -1
			isDown = True
		if code not in codes:
			codes[code] = 1.0
		else:
			codes[code] += 1.0
		if speed != None:
			if code not in times:
				times[code] = speed
			else:
				times[code] += speed
		if (isDown):
			if (interval != 0):
				all_intervals.append(interval)
			interval = 0

	if (not isDown):
		all_intervals.append(interval)

	return times, codes, all_intervals



def pct_avail(data):
	
	total = sum(data.values())
	avail = 0.0

	for code in data.keys():
		if code > 0:
			avail += data[code]

	return (avail / total) * 100



def average(array):
	n = len(array) * 1.0
	return sum(array) / n



def print_out(url, timespan):

	url_data = get_stats(url, timespan)
	times = url_data[0]
	codes = url_data[1]
	intervals = url_data[2]
	percent_up = min(100.0 * sum(intervals) / timespan, 100)
	
	print ""
	print "visiting: " + url
	print times
	print codes
	print intervals
	print "percent up: " + str(percent_up) + "%"
	print ""
	return "success"


def parallel(args):
	return print_out(*args)



def main():
	
	url_in = raw_input("input a url, for multiple - separate by commas: ")
	min_in = int(raw_input("input amount of minutes for interval: "))
	sec_in = int(raw_input("input amount of seconds for interval: "))
	
	timespan = (min_in * 60) + (sec_in)
	url_in = url_in.split(',')
	n = len(url_in)
	for i in range(n):
		url_in[i] = (url_in[i].strip(), timespan) 

	while (1):
		p = mp.Pool(5)
		print "(re)initializing"
		print p.map(parallel, url_in)
	
	return



if __name__ == "__main__":
	main()



