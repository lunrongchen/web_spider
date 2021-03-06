from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from sinaRss.items import NewsMarqueDdtItem
from sinaRss.items import SinaRssItem
from sinaRss.items import contentItem
from scrapy.http import Request
from scrapy.http import HtmlResponse
from readability.readability import Document as Doc
import psycopg2
import xmltodict
import codecs
import json
from lxml import html
import sys
from Naked.toolshed.shell import muterun_js


class baiduNewsSpider( CrawlSpider ):
    name = 'baidu'

    start_urls = []

    configDict = {}

    fileptr = None
    
    conn = None
    cur = None

    def op( self, str ):
        self.fileptr.write ( str )
        

    def __init__( self ):
        self.conn = psycopg2.connect("dbname=news user=bdccl")
        self.cur = self.conn.cursor()
        self.fileptr = codecs.open( self.name + ".logfile", "w", 'utf-8' )

        #todo
        # need to edit config file

        readin = codecs.open( 'sinaRss/spiders/baidu_config.txt', "r", "utf-8" )
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


    	

        print "endParse\n\n\n"

        print response.url

        xmldata = response.body
        
        t_unicode = xmldata.decode( response.encoding )
        xmldata = t_unicode.encode('utf-8')

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
                
                self.conn.commit()
                self.cur.execute('insert into baidurss( url, title, pubDate, pubTime, description, rss) values( %s, %s, %s, %s, %s, %s )', (link, title, date, time, desc, response.url ))
                self.conn.commit()

                print 'a1'
                req = Request( rssItem['link'], self.articleParse )
                print 'a2'
                req.meta['url'] = link
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
        print '\n\n\n\narticleParse\n' + response.meta['url']
        #self.op( '\n\n\n' +  response.url + '\n' + response )
        #print response.__dict__
        #sel = HtmlXPathSelector( response )

        doc = response.body.decode( response.encoding )
    	content = ""
    	title = ""
    	try:
    		content = Doc( doc).summary()
    		title = Doc(doc).short_title()
    		print content
    	except:
    		print "err at parseArticle"
    		return


        #print response.body
        #fpt = codecs.open('tmp.html','w', 'utf-8')
        #fpt.write ( response.body.decode( response.encoding).encode('utf-8'))
        #fpt.write ( response.body.decode( response.encoding) )
        #jsresponse = muterun_js("ParseContent.js")
        #content = ""
        #title = ""
    	#if jsresponse.exitcode==0:
    	#	obj = json.loads((jsresponse.stdout))
    	#	title = obj['title']
    	#	content = obj['content']
    	#	print content
    	#else:
    	#	sys.stderr.write(jsresponse.stderr)
    	#	pass

        """
        tree = html.fromstring(response.body.decode( response.encoding))

        xpathStr = response.meta ['xpath']

        r = tree.xpath( xpathStr )
        
        _str = ""
        for x in r:
            _str+= " " + x
        """

        item = contentItem()
        item['url'] = response.meta['url']
        item['content'] = content
        self.op( '\n\n\n' )
        self.op( response.url )
        self.op( content )
        
        try:
			print ("getin");
			self.conn.commit()
			self.cur.execute('insert into baiducontent( url, title, content ) values( %s,%s, %s )', ( item['url'], title, content))
			self.conn.commit()
			print "getout"
        except:
            print 'error!!!! at articleParse'
            pass

        print '++++++++++++++++\n'

        return item
        
