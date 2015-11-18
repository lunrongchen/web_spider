from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from daily.items import RssItem
from daily.items import ContentItem
from scrapy.http import Request
from scrapy.http import HtmlResponse
from readability.readability import Document as Doc
import psycopg2
import xmltodict
import codecs
import json
from lxml import html
import sys


class baiduNewsSpider( CrawlSpider ):
    name = 'baidu'

    start_urls = []

    configDict = {}

    fileptr = None

    conn = None
    cur = None        

    def __init__( self ):

        # connect with data base

        self.conn = psycopg2.connect("dbname=news2 user=bdccl")
        self.cur = self.conn.cursor()
        #self.fileptr = codecs.open( self.name + ".logfile", "w", 'utf-8' )

        # read rss address list file
        readin = codecs.open( 'daily/spiders/baidu_config.txt', "r", "utf-8" )
        for rss in readin.readlines():
            if rss == "":
                break;
            try:
                obj = json.loads( rss )
            except:
                break
            self.start_urls.append( obj['url'] )
            self.configDict[ obj['url'] ] = obj

    def parse( self, response ):

        xmldata = response.body
        
        t_unicode = xmldata.decode( response.encoding )
        xmldata = t_unicode.encode( 'utf-8' )

        dict = xmltodict.parse( xmldata, encoding='utf-8' )
        rssItems = dict['rss']['channel']['item']
        
        NewsList = []

        for rssItem in rssItems:
            title = rssItem['title']
            link = rssItem['link']
            pubDate = rssItem['pubDate']
            desc = rssItem['description']
            print title
            print rssItem
            #print '-------------'

            date = "19700101"
            time = "12:53:83"

            if pubDate != None:
                conf = self.configDict[response.url]

                #time = pubDate[11:19]
                #year = pubDate[0:4]
                #mon = pubDate[5:7]
                #day = pubDate[8:10]

                #todo
                #need to edit time step

                #time = pubDate[ conf['timestart'] : conf['timeend']]
                #year = pubDate[ conf['yearstart'] : conf['yearend']]
                #mon = pubDate[ conf['monthstart'] : conf['monthend']]
                #day = pubDate[ conf['daystart'] : conf['dayend']]

                #hour = ...
                #minute = ...
                #second  = pubDate[ .. : ..]
                #time = hour +":" + minute + ":" + second

                print pubDate
                tmp1 = pubDate.split("T")
               	date = tmp1[0]
                time = tmp1[1][:-5]
                print date, time

            #self.op( "\n\n\n" )
            #self.op( "title:\t" + title )
                #self.op ( [link , date, time, weekday].__str__() )
                #self.op( 'desc:\t' + desc )

                
            try:
                #print "%s+%s+%s+%s+%s+%s" %( link, title, date, time, weekday, desc)
                print "%s-%s-%s" % (link, title, pubDate)
                
                self.conn.commit()
                print '1'
                #self.cur.execute('insert into baidurss(url, title, pubdate, pubtime, pubtimestamp, description, rssline) values ( %s, %s, %s, %s, %s, %s, %s, %s )', (link, title, date, time, pubtimestamp, desc, response.url) )
                self.cur.execute('insert into baidurss(url, title, pubdate, pubtime, pubtimestamp, description,rssline ) values(%s,%s,%s, %s,%s,%s, %s)', (link, title, date,time, pubDate, desc, response.url))
                #self.cur.execute('insert into baidurss( url, title, pubDate, pubTime, description, rss) values( %s, %s, %s, %s, %s, %s )', (link, title, date, time, desc, response.url ))
                print '2'
                self.conn.commit()

                print 'a1'
                req = Request( rssItem['link'], self.articleParse )
                print 'a2'
                req.meta['url'] = link
                req.meta['pubDate'] = pubDate
                req.meta['title'] = title
                #req.meta['xpath'] = self.configDict[response.url]['xpath']
                print 'a2'
                yield req
            except psycopg2.Error as e:
                print e.pgerror
                print 'error!!! at parse'
                pass
            except:
                print 'no'
                pass
            pass
            
    def articleParse( self, response ):
        print '\n\n\n\narticleParse\n' + response.meta['url'] + response.meta['pubDate']
        #self.op( '\n\n\n' +  response.url + '\n' + response )
        #print response.__dict__
        #sel = HtmlXPathSelector( response )

        url = response.meta['url']
        time = response.meta['pubDate']
        title = response.meta['title']
        doc = response.body.decode( response.encoding )

        try:

            print "getin"

            self.conn.commit()
            print url , time
            #self.cur.execute('insert into rawpage(url) values(%s)',(url))
            self.cur.execute('insert into rawpage(pubtime, title, url, raw) values(%s, %s, %s, %s)', (time, title, url, doc));
            self.conn.commit()

            print "getout"
        except:
            print "error ! article parse"
            pass

        return ContentItem()

