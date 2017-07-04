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
f.write('{"D":"4", "T":"20"}\n')
f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "a1", "id2": "a2"}\n')
f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "a2", "id2": "a3"}\n')
f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "a2", "id2": "a4"}\n')

f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "b1", "id2": "b2"}\n')
f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "b2", "id2": "b3"}\n')
f.write('{"event_type":"befriend", "timestamp":"2017-06-13 11:33:01", "id1": "b3", "id2": "b4"}\n')

# Here batch_log contains only befriend and unfriend
nentries=1000
# Add 1000 purchases for a1,a2,a3 and a4, of amounts ranging from 1 to 10
for ii in range(nentries):
    uid="a"+str(random.randrange(1,5,1)) #random number between 1 and 4
    amount=random.randrange(1,10) #random number between 1 and 10
    timestamp=randomDate("2008-06-13 01:30:01", "2009-06-13 13:50:03", random.random())
    purchase={
    "id": uid, 
    "amount": amount,
    "event_type": "purchase",
    "timestamp": timestamp,
    "id": uid,
    "amount": amount}
       
    f.write("{}\n".format(dumps(purchase)))

# Here batch_log contains only befriend and unfriend
nentries=1000
# Add 1000 purchases for b1,b2,b3 and b4, of amounts ranging from 100 to 1000
for ii in range(nentries):
    uid="b"+str(random.randrange(1,5,1)) #random number between 1 and 4
    amount=random.randrange(100,1000) #random number between 100 and 1000
    timestamp=randomDate("2008-06-13 01:30:01", "2009-06-13 13:50:03", random.random())
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
    uid="a"+str(random.randrange(1,5,1)) #random number between 1 and 4
    amount=random.randrange(1,10) #random number between 1 and 10
    timestamp=randomDate("2008-06-13 01:30:01", "2009-06-13 13:50:03", random.random())
    purchase={
    "id": uid, 
    "amount": amount,
    "event_type": "purchase",
    "timestamp": timestamp,
    "id": uid,
    "amount": amount}
       
for ii in range(nentries):
    uid="b"+str(random.randrange(1,5,1)) #random number between 1 and 4
    amount=random.randrange(100,1000) #random number between 100 and 1000
    timestamp=randomDate("2008-06-13 01:30:01", "2009-06-13 13:50:03", random.random())
    purchase={
    "id": uid, 
    "amount": amount,
    "event_type": "purchase",
    "timestamp": timestamp,
    "id": uid,
    "amount": amount}
    f.write("{}\n".format(dumps(purchase)))

# Now add a few additional "flagged" purchases (flagged only for class a):
nentries=5
for ii in range(1,nentries):
    uid="a"+str(ii)
    amount=random.randrange(100,1000) #random number between 100 and 2000
    purchase={
    "id": uid, 
    "amount": amount,
    "event_type": "purchase",
    "timestamp": timestamp,
    "id": uid,
    "amount": amount}
    f.write("{}\n".format(dumps(purchase)))

    uid="b"+str(ii)
    purchase['id']=uid
    f.write("{}\n".format(dumps(purchase)))

f.close()
