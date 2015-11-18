from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from sinaRss.items import NewsMarqueDdtItem
from sinaRss.items import SinaRssItem
from sinaRss.items import contentItem
from scrapy.http import Request
from scrapy.http import HtmlResponse
import psycopg2
import xmltodict
import codecs
import json
from lxml import html

class AllNewsSpider( CrawlSpider ):
    name = 'renmin'

    start_urls = []
    #start_urls = ['http://rss.sina.com.cn/news/world/focus15.xml']

    configDict = {}

    fileptr = None
    
    conn = None
    cur = None

    def op( self, str ):
        self.fileptr.write ( str )
        

    def __init__( self ):
        self.conn = psycopg2.connect("dbname=news user=carwest ")
        self.cur = self.conn.cursor()
        self.fileptr = codecs.open( self.name + ".logfile", "w", 'utf-8' )

        #todo
        # need to edit config file

        readin = codecs.open( 'sinaRss/spiders/renmin_rss_config.txt', "r", "utf-8" )
        for rss in readin.readlines():
            obj = json.loads( rss )
            self.start_urls.append( obj['url'] )
            self.configDict[ obj['url'] ] = obj


    def parse( self, response ):

        print response.url
        #print self.encodeDict[response.url]

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
            desc = ""
            print title
            print '-------------'

            date = 0
            time = 0

            if pubDate != None:
                conf = self.configDict[response.url]
                #print conf

                #time = pubDate[11:19]
                #year = pubDate[0:4]
                #mon = pubDate[5:7]
                #day = pubDate[8:10]
                weekday = ""

                #todo
                #need to edit time step

                time = pubDate[ conf['timestart'] : conf['timeend']]
                year = pubDate[ conf['yearstart'] : conf['yearend']]
                mon = pubDate[ conf['monthstart'] : conf['monthend']]
                day = pubDate[ conf['daystart'] : conf['dayend']]

                
                
                #minute = ...
                #second  = pubDate[ .. : ..]
                #time = hour +":" + minute + ":" + second

                date = year+"-"+mon+"-"+day



                self.op( "\n\n\n" )
                self.op( "title:\t" + title )
                self.op ( [link , date, time, weekday].__str__() )
                self.op( 'desc:\t' + desc )

                
                try:
                    #print "%s+%s+%s+%s+%s+%s" %( link, title, date, time, weekday, desc)
                    if link == None or title == None or date == None or time == None or weekday == None or desc == None:
                        print 'nonononono!!!'

                    self.conn.commit()
                    self.cur.execute('insert into allrss( url, title, pubDate, pubTime, description, rss) values( %s, %s, %s, %s, %s, %s )', (link, title, date, time, desc, response.url ))
                    self.conn.commit()
                except psycopg2.Error as e:
                    print e.pgerror
                    print 'error!!! at parse'
                    pass
                except:
                    print 'no'
                    pass

            yield Request( rssItem['link'], self.articleParse )

    def articleParse( self, response ):
        print '\n\n\n\narticleParse'
        #self.op( '\n\n\n' +  response.url + '\n' + response )
        #print response.__dict__
        #sel = HtmlXPathSelector( response )
        doc = response.body
        tree = html.fromstring(response.body.decode( response.encoding))

        xpathStr = "";
        try:
            self.conn.commit()
            self.cur.execute('select rss from allrss where url = %s;', (response.url,))
            rss = self.cur.fetchone()[0]
            self.conn.commit()
            
        except:
            print 'error at pass article find rss'
            pass
        
        xpathStr = self.configDict[rss]['xpath']
        #print xpathStr
        
    

        #r = tree.xpath('//*[@id="Cnt-Main-Article-QQ"]/p/text()')
        r = tree.xpath( xpathStr )
        #print r[0]

        #l = sel.xpath('//*[@id="artibody"]/p/text()').extract()
        #l = sel.xpath('//*[@id="Cnt-Main-Article-QQ"]/p/text()').extract()


        
        _str = ""
        for x in r:
            _str+= " " + x

        item = contentItem()
        item['url'] = response.url
        item['content'] = _str
        self.op( '\n\n\n' )
        self.op( response.url )
        self.op( _str )
        
        try:
            self.conn.commit()
            self.cur.execute('insert into allcontent( url, content ) values( %s, %s )', ( response.url, _str ))
            self.conn.commit()
        except:
            print 'error!!!! at articleParse'
            pass

        print '++++++++++++++++\n'

        yield item

