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


# 1) Make batch_log file
f= open("batch_log.json","w")
# First add to batch_log only befriend and unfriend events:
f.write('{"D":"2", "T":"20"}\n')
f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "1", "id2": "2"}\n')
f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "1", "id2": "3"}\n')
f.write('{"event_type":"unfriend", "timestamp":"2017-06-13 11:33:01", "id1": "1", "id2": "3"}\n')
f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "2", "id2": "3"}\n')
f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "2", "id2": "4"}\n')
f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "3", "id2": "4"}\n')

# Here batch_log contains only befriend and unfriend
nentries=1000

timestamp="2017-07-04 00:00:00"

for ii in range(nentries):
    uid=random.randrange(1,5,1) #random number between 1 and 4
    amount=random.randrange(1,10) #random number between 1 and 10
    #timestamp=randomDate("2008-06-13 01:30:01", "2009-06-13 13:50:03", random.random())
    purchase={
    "id": uid, 
    "amount": amount,
    "event_type": "purchase",
    "timestamp": timestamp,
    "id": uid,
    "amount": amount}
       
    f.write("{}\n".format(dumps(purchase)))
f.close()

#Now let's fill stream_log.json
f= open("stream_log.json","w")
nentries=100
for ii in range(nentries):
    uid=random.randrange(1,5,1) #random number between 1 and 4
    amount=random.randrange(1,10) #random number between 1 and 10
    #timestamp=randomDate("2008-06-13 01:30:01", "2009-06-13 13:50:03", random.random())
    purchase={
    "id": uid, 
    "amount": amount,
    "event_type": "purchase",
    "timestamp": timestamp,
    "id": uid,
    "amount": amount}
       
    f.write("{}\n".format(dumps(purchase)))
# Now add a few additional "flagged" purchases:
nentries=5
for ii in range(1,nentries):
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
