
import requests as rq
import time
import threading as th
import multiprocessing as mp



def get_stats(url, timespan):
	
	begin = time.time()			# begging time for entire function
	codes = dict()				# http code mapped to total occurrences
	times = dict()				# http code mapped to sum of req durations
	times_list = list()			# request durations
	all_intervals = list()		# up and down times
	isDown = False;				# flag to modify time if site is down
	speed = None;				# in case website is never up / dne
	LW = 3						# multiplier for urlopen timeout
	interval = 0				# initialize time interval of site being up

	duration = time.time() + timespan	# one minute	
	while (time.time() < duration):
		try:
			if (len(times_list) != 0):
				TO = max(times_list)
				start = time.time()
				rq.get(url, timeout = TO * LW)
				speed = time.time() - start
				times_list.append(speed)
			else:
				start = time.time()
				url_open = rq.get(url)
				url_open
				speed = time.time() - start
				times_list.append(speed)
			code = url_open.status_code
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

	return times, codes, all_intervals, times_list



def pct_avail(data):
	
	total = sum(data.values())
	avail = 0.0

	for code in data.keys():
		if code > 0:
			avail += data[code]

	return (avail / total) * 100



def average(array):
	n = len(array) * 1.0	
	if int(n) != 0:
		return sum(array) / n
	else:
		return 0



def print_out(url, timespan):

	url_data = get_stats(url, timespan)
	times = url_data[0]
	codes = url_data[1]
	intervals = url_data[2]
	percent_up = min(100.0 * sum(intervals) / timespan, 100)
	all_times = url_data[3]

	try:
		del times[-1]
	except KeyError:
		pass
	try:
		del codes[-1]
	except KeyError:
		pass
	time_up = sum(times.values())
	tot_req = sum(codes.values())

	print ""
	print "Visiting: " + url
	print "Interval: " + str(timespan) + "s"
	print "Total requests: " + str(int(tot_req))
	try:
		print "Fastest request: " + str(min(all_times)) + "s"
	except ValueError:
		pass
	try:
		print "Slowest request: " + str(max(all_times)) + "s"
	except ValueError:
		pass
	print "Average request time: " + str(average(all_times)) + "s"
	print "Total time per status code: " + str(times)
	print "Total requests per status code: " + str(codes)
	print "Site down for: " + str(max(timespan- sum(intervals), 0)) + "s"
	if percent_up < 80:
		print "!!! ALERT !!!"
		print "Website " + str(url) + " is down." 
		print "!!! ALERT !!!"
		print "Availability = " + str(percent_up) + "%"
		print "Time up: " + str(time_up) + "s. Time down: " + str(max(0, 
			timespan - time_up)) + "s"
	else:
		print "Percent up: " + str(percent_up) + "%"
		print "Time up: " + str(time_up) + "s. Time down: " + str(max(0, 
			timespan - time_up)) + "s"
	print ""

	return "Successful iteration"



def parallel(args):
	return print_out(*args)



def main():
	
	url_in = raw_input("input a url, for multiple - separate by commas: ")
	min_in = int(raw_input("input amount of minutes for interval: "))
	sec_in = int(raw_input("input amount of seconds for interval: "))
	
	timespan = (min_in * 60) + (sec_in)
	largerspan = 1 * 60
	url_in = url_in.split(',')
	n = len(url_in)
	for i in range(n):
		url = url_in[i].strip()
		url_in[i] = (url, timespan)


	while (1):
		p = mp.Pool(5)
		print "(re)initializing"
		print p.map(parallel, url_in)
	
	return



if __name__ == "__main__":
	main()


# https://www.datadoghq.com, http://www.apple.com
