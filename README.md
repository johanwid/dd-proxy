# dd-proxy
a simple 'proxy' that checks basic website stats


HOWTO:

Note: I wrote this in MacOS

Below is a basic example of how to run the .py file

Open up Terminal/Commandline/etc

run the program
unix> python test.py
input desired websites to monitor
unix> https://www.apple.com, https://www.google.com, https://www.youtube.com
input amount of minutes for interval
unix> 10
input amount of seconds for interval
unix> 30

and then wait for the outputs.


NOTES:

As of right now, the calculated stats are only based on one uniform time interval.
Based on the email/spec sheet, I was unsure if we were supposed to do it this way,
but, in theory, it should be possible to allow for multiple windows of stats to
be shown. 

The websites are visited in parallel using Python's "multiprocessing" library in 
order to prevent "stacking" of website visits.


IMPROVE:

For the sake of UX, I think it'd be for the best to have some sort of GUI to make
it more legible on the user's part to view the data.

Something that could be interesting is allowing the user to always request new
websites to monitor, which would probably be done by allowing 'raw_input()' to 
always be running in the background.

Make it more pleasent to quit out of the program instead of relying on signals and
keyboard binds.  This could also potentially rely on always allowing 'raw_input()'
to always be running and waiting for "quit" to be inputted or something similar.

Think about more interesting stats to display/calculate.

Comments.  I should probably comment my code more (effectively).

And, of course, work on performance.  I wrote this during finals week, so didn't
get to focus on performance as much as I would have liked, for better or worse,
but I'm sure there are countless things that I could have optimized.
