#!/bin/python2
# -*- encoding:utf-8 -*-

import psycopg2

conn = psycopg2.connect("dbname=news2 user=bdccl")
cur = conn.cursor()

#wait for the lock

import time
import random
lock = True

while lock:
	conn.commit()
	cur.execute("select lock from filterlock")
	lock = cur.fetchone()[0]

	if lock :
		print "waiting"
		time.sleep(random.random())
	else :
		conn.commit()
		#cur.execute("update filterlock set lock=True where id = 1")
		lock = False
		conn.commit()
		break

conn.commit()
cur.execute("select cnt from filterlock")
targ1 = cur.fetchone()[0]
conn.commit()

cur.execute("select max(id) from  page");
targ2 = cur.fetchone()[0]
conn.commit()


cur.execute("select * from page where id > %s and id <= %s", (targ1, targ2))

raws = cur.fetchall()
conn.commit()


cur.close()
conn.close()

## filter


import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

conn = psycopg2.connect("dbname=news2 user=bdccl")
cur = conn.cursor()

from event_label import Event
from location_label import Location

ev = Event()
lc = Location()


for line in raws:

	idx = line[0]
	title = line[1]
	content = line[2]
	url = line[3]
	time = line[4]

	try:
		content = content.decode('utf-8')
		
		eve = ev.label(content)
		loc = lc.label(content)
		
		eve = "no"

		#print eve, loc

		#if eve[1] != None and loc[1] != None:
		if loc[1] != None:
			#print content
			conn.commit()
			print idx, title, eve[1], loc[1]
			tpl = ( idx, title, content, url, time, eve[1], loc[1] )
			cur.execute( "insert into labeled(id, title, content, url, pubtime, event, location) values(%s, %s, %s, %s, %s, %s, %s)", tpl )
			conn.commit()
	except:
		conn.commit()
		pass




conn.commit()
cur.execute("update filterlock set lock=False where id=1")
conn.commit()
cur.execute("update filterlock set cnt = %s where id = 1", (targ2, ))
conn.commit()

cur.close()
conn.close()

