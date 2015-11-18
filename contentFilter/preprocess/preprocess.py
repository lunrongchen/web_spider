# coding=utf-8

__author__ = 'carwest'
# -*- encoding=utf-8 -*-

import psycopg2
import jieba
import codecs
import json
from lxml import etree

class Preprocess:
    KEYWORDS = [u"聚众", u"强占", u"强征", u"强拆", u"非法集会", u"大众恐慌", u"骚乱", u"集会", u"集体怠工", u"集体上访", u"游行示威", u"示威", u"抗议",u"罢工",u"罢课",u"哄抢",u"斗殴",u"闹事",u"暴乱",u"暴动",u"劫机",u"劫船",u"劫持",u"暴力性犯罪"，u"暴力群斗"，u"宗教冲突"，u"恶性侵犯"]


    def __init__(self):
        self.conn = psycopg2.connect("dbname=news user=bdccl")
        self.cur = self.conn.cursor()
        self.filePtr = None
        self.cnt = 0

    def all(self):
        self.conn.commit()
        self.cur.execute("select * from allcontent as all full join allrss on all.url = allrss.url where pubdate > date '20150501'")
        #self.filePtr = codecs.open('selected_all.txt', 'w', 'utf-8')
        for record in self.cur.fetchall():
            #print record[2]
            try:
                print record
                content = record[1]
                #print content
                seglist = jieba.cut(content)
                for word in seglist:
                    flag = False
                    for keyword in self.KEYWORDS:
                        if word == keyword:
                            flag = True
                            print content
                            #self.filePtr.write(json.dumps({"content": content}) + "\n")
                            self.cnt += 1
                            self.cur.execute("insert into basicwords(pubdate,pubtime,location,content,title,matchedwords) values(%s,%s,%s,%s,%s,%s)",(record[4],record[5],'北京',record[1],record[3],word))
                            break
                    if flag:
                        break

            except:
                print "some error"

        self.conn.commit()

    def baidu(self):
        #self.filePtr = codecs.open('selected.txt', 'w', 'utf-8')
        self.conn.commit()
        self.cur.execute("select * from baiducontent right join (select * from baidurss where pubdate>current_date-Integer '1' ) as rss on baiducontent.url = rss.url  limit 10000 ")
        cnnt = 0
        try:
            while True:
                #for record in self.cur.fetchall():
                record = self.cur.fetchone()
                if not record:
                    break
                cnnt += 1
                if ( cnnt % 1000 == 0 ):
                    print "%d" % cnnt
                #print record[2]
                try:
                    root = etree.fromstring(record[2])
                    contentList = root.xpath("//descendant-or-self::*/text()")
                    content = ""
                    for part in contentList:
                        content += " " + part
                    #print content
                    seglist = jieba.cut(content)
                    for word in seglist:
                        flag = False
                        for keyword in self.KEYWORDS:
                            if word == keyword:
                                flag = True
                                print record[1] 
                                #print record[2],record[6],record[0],word
                                #self.filePtr.write(json.dumps({"title": record[1], "content": content}) + "\n")
                                self.cur.execute("insert into basicwords(pubdate,pubtime,location,title,content,matchedwords) values(%s,%s,%s,%s,%s,%s)",(record[5],record[6],'北京',record[1],record[2],word))
                                self.conn.commit()

                                self.cnt += 1
                                break
                        if flag:
                            break
                except:
                    print "some error"

            self.conn.commit()
        except:
            print 'end'



if __name__ == "__main__":
    pre = Preprocess()
    pre.baidu()
    # sepre.all()
    print pre.cnt



