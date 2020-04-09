import scrapy
import deltai.frequency as frequency
import w3lib.html
import re
from app import  db, models

class NewsSpider(scrapy.Spider):
    name = 'news'

    def start_requests(self):
        meta = {}
        for newspaper in  models.Newspaper.query.all() :
            if newspaper.id == 1 :
                meta = {'news-in-page' : 'div.views-row', 'menu' : 'ul.menu', 'sections' : 'li.leaf a', 'body' : 'div.field-name-body'  }
            
            if newspaper.id == 3 :
                meta = {'news-in-page' : 'div.ljn-row', 'menu' : 'ul.navbar-nav', 'sections' : 'li.nav-item a', 'body' : 'div.ljn-nota-contenido'}
                
            if newspaper.id == 2 :
                meta = {'news-in-page' : 'div.teaser', 'menu' : 'ul.navbar-nav', 'sections' : 'li.dropdown a', 'body' : 'div.content-body'}

            meta['newspaper'] = newspaper
            yield scrapy.Request(url=newspaper.url, callback=self.parse, meta=meta)

    def parse(self, response):
        for news in response.css(response.meta.get('news-in-page')) :
            for h in news.css('h1,h2,h3,h4,h5'):
                try :
                    title =  h.css('a::text').get()
                    href = h.css('a::attr(href)').get()
                    news = models.News(url=href, title=title, newspaper_id=response.meta.get('newspaper').id)  
                    try : 
                        models.News.query.filter_by(url=href).one()   
                    except Exception as e:
                        meta = {**{'title' :title, 'href' : href, 'news':news}, **response.meta}
                        yield response.follow(href, self.parse_news, meta=meta)
                        pass
                except Exception as e :
                    print(e)
        if response.meta.get('repeat', True) :                    
            section_div = response.css(response.meta.get('menu'))
            sections= section_div.css(response.meta.get('sections'))
            meta = {**{'repeat' : False}, **response.meta}
            yield from response.follow_all(sections, self.parse, meta=meta)


                    
    def parse_news(self, response) :
        try :
            body_news = response.css(response.meta.get('body'))
            text = w3lib.html.replace_entities(w3lib.html.replace_escape_chars(w3lib.html.remove_tags(' '.join(body_news.extract()))))
            text =re.compile(r'\W+', re.UNICODE).split(text.lower())
            text = ' '.join(text)
            news = response.meta.get('news')
            news.content = text
            #db.session.add(news)
            words = frequency.get_frequency([text, response.meta.get('title')])
            tags = words.pop(0).to_dict()
            for stock in words :
                for key, value in stock.to_dict().items() :
                    if key in tags :
                        tags[key] += value
                    else :
                        tags[key] = value
            for tag, value in tags.items() :
                try :
                    tag = models.Tag.query.filter_by(name=tag).one()
                except Exception as e :
                    tag = models.Tag(name=tag)
                    #db.session.add(tag)
                if value > 0 :
                    db.session.add(models.NewsTag(news=news, tag=tag, rank=value))
            db.session.commit()
            yield {
                'title' : response.meta.get('title'),
                'href' : response.meta.get('href'),
            }
        except Exception as e :
            print(e)


        