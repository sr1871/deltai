import os
import sys

from flask import Flask, request, jsonify
#from deltai.spiders.news_spider import NewsSpider
#from twisted.internet import reactor
#import scrapy
#from scrapy.crawler import CrawlerRunner
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import distinct
from sqlalchemy.orm import join

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres@db/deltai"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app
app = create_app()
db = SQLAlchemy(app)

import models


# a simple page that says hello
@app.route('/api/news', methods=['POST',])
def hello():
    data = request.get_json()
    if 'keywords' in  data:
        keywords = [x.lower() for x in data.get('keywords', [])]
        tags_ids = list_id(models.Tag.query.filter(models.Tag.name.in_(keywords)))
        news_ids = db.session.query(
                models.NewsTag.news_id, 
                func.sum(models.NewsTag.rank).label('total'),
                ).\
            select_from(join(models.NewsTag, models.News)).\
                distinct(models.News.newspaper_id).\
            filter(models.NewsTag.tag_id.in_(tags_ids), models.News.content != '').\
            group_by(models.NewsTag.news_id, models.News.newspaper_id).\
            order_by(models.News.newspaper_id, func.sum(models.NewsTag.rank).desc()).all()
        news_ids = dict(news_ids)
        response_news = models.News.query.filter(models.News.id.in_(news_ids.keys()))
        news_return = []
        for news in response_news :
            news_return.append({
                'ranking' : (news_ids.get(news.id) / len(tags_ids)) * 2,
                'title' : news.title,
                'content' : news.content,
                'reference' :  news.url if '://' in news.url else (news.newspaper.url + '/' + news.url)
            })
        news_return.sort(key=lambda x : x.get('ranking', 0), reverse=True)
        return jsonify({
            "news" : news_return
        })

        

    return jsonify({
            "error" : 'need tags parameter'
        }), 400


def list_id(objs) :
    return [obj.id for obj in objs]
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3002, debug=True)
