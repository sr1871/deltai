from app import db
from sqlalchemy.dialects.postgresql import JSON



class Newspaper(db.Model) : 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    news = db.relationship('News', back_populates='newspaper', lazy=True)

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    newspaper_id = db.Column(db.Integer, db.ForeignKey('newspaper.id'), nullable=False)
    newspaper = db.relationship('Newspaper', back_populates='news', lazy=True)
    news_tags = db.relationship('NewsTag', back_populates='news', lazy=True)

    def __init__(self, url, title, content= '', newspaper_id=None):
        self.url = url
        self.title = title
        self.content = content
        self.newspaper_id = newspaper_id

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    news_tags = db.relationship('NewsTag', back_populates='tag', lazy=True)

    def __init__(self, name):
        self.name = name

class NewsTag(db.Model) :
    __tablename__ = 'news_tag'

    id = db.Column(db.Integer, primary_key=True)
    news = db.relationship('News', back_populates='news_tags', lazy=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    tag = db.relationship('Tag', back_populates='news_tags', lazy=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    rank = db.Column(db.Float, default=0)

    def __init__(self, news, tag, rank):
        self.news = news
        self.tag = tag
        self.rank =rank

