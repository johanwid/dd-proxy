
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


import urllib as ul
import time
import multiprocessing as mp

def average(array):
	n = len(array) * 1.0
	return sum(array) / n

def code_count(url, mins, secs):
	
	head = ['http://', 'https://']
	data = dict()
	times = list()

	if (url[0:7] not in head):
		return "invalid address. must begin with 'http://'"

	duration = time.time() + (mins * 60) + (secs)
	while (time.time() < duration):
		start = time.time()
		code = ul.urlopen(url).getcode()		# http status code
		speed = time.time() - start
		times.append(speed)
		if code not in data:
			data[code] = 1.0
		else:
			data[code] += 1.0
	
	return average(times), sum(times), data

def pct_avail(data):
	
	good = [200, 202]
	total = sum(data.values())
	avail = 0.0

	for code in data.keys():
		if code in good:
			avail += data[code]

	return (avail / total) * 100


url_in = raw_input("input a url to check status of: ")
min_in = raw_input("input amount of minutes: ")
sec_in = raw_input("input amount of seconds: ")

url_data = code_count(url_in, int(min_in), int(sec_in))[2]

print url_data
print pct_avail(url_data)

"""
output dashboard, include interesting parts of information
add parallelization for multiple websites
run an outer while loop that does the 10 minute check in the background
"""



