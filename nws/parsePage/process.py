import psycopg2

conn = psycopg2.connect("dbname=news2 user=bdccl")
cur = conn.cursor()



#wait for the lock

import time
import random
lock = True

while lock :
    conn.commit()
    cur.execute("select lock from process")
    lock = cur.fetchone()[0]


    
    if lock:
        print "waiting"
        time.sleep(random.random())
    else :
        conn.commit()
        cur.execute("update process set lock=True where id=1")
        conn.commit()
        break



cur.execute("select cnt from process");
targ1 = cur.fetchone()[0]
conn.commit()

cur.execute("select max(id) from rawpage");
targ2 = cur.fetchone()[0]
conn.commit()

print targ1, targ2





cur.execute("select * from rawpage where id > %s and id <= %s", (targ1, targ2) );
raws = cur.fetchall()
conn.commit()

cur.close()
conn.close()



#start to process

conn = psycopg2.connect("dbname=news2 user=bdccl")
cur = conn.cursor()

from readability.readability import Document as Doc
from bs4 import BeautifulSoup


for line in raws:
    idx = line[0]
    time = line[1]
    url = line[2]
    raw = line[3]
    title = line[4]
    print idx, time, url, title

    try:
        content = Doc(raw).summary()
        content = BeautifulSoup(content).get_text()

        conn.commit()
        cur.execute("insert into page(id, title, content, url, pubtime) values( %s, %s, %s, %s, %s)", (idx, title, content, url, time)) 
        conn.commit()
    except:
        conn.commit()
        pass



conn.commit()
cur.execute("update process set lock=False where id=1")
conn.commit()
cur.execute("update process set cnt = %s where id = 1",  (targ2,) )
conn.commit()

cur.close()
conn.close()
