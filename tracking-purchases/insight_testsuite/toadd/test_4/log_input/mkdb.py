from json import dumps
import random


import time

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y-%m-%d %H:%M:%S', prop)


# Here batch_log contains only befriend and unfriend
nentries=100
f= open("stream_log.json","w")

for ii in range(nentries):
    uid=random.randrange(1,10,1) #random number between 1 and 10
    amount=random.randrange(1,10) #random number between 1 and 10
    #timestamp=randomDate("2008-06-13 01:30:01", "2009-06-13 13:50:03", random.random())
    timestamp="2008-06-13 00:00:00"
    purchase={
    "id": uid, 
    "amount": amount,
    "event_type": "purchase",
    "timestamp": timestamp,
    "id": uid,
    "amount": amount}
       
    f.write("{}\n".format(dumps(purchase)))

# Now add a few additional "flagged" purchases:
nentries=10
for ii in range(nentries):
    uid=ii
    amount=random.randrange(100,2000) #random number between 100 and 2000
    purchase={
    "id": uid, 
    "amount": amount,
    "event_type": "purchase",
    "timestamp": timestamp,
    "id": uid,
    "amount": amount}
       
    f.write("{}\n".format(dumps(purchase)))

f.close()
