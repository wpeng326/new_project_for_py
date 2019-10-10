from models.blog import Blog, FriendlyLink, Article, ArticleType
from utils.log import Logger

server_error = '服务器开小差了。。。'

def footer_info(self):
    try:
        blog_obj = Blog.get(Blog.id == 1)
        footer_text = blog_obj.copyright
        return footer_text
    except Exception as e:
        Logger().log(e, True)
        return server_error


def get_title_data(self, info):
    try:
        blog_obj = Blog.get(Blog.id == 1)
        if info == 'title':
            title_data = blog_obj.title
        elif info == 'site':
            title_data = blog_obj.site
        else:
            return server_error
        return title_data
    except Exception as e:
        Logger().log(e, True)
        return server_error


def frindly_link(self):
    try:
        blog_objs = FriendlyLink.select().order_by(FriendlyLink.weight)
        pg_html = ""
        for obj in blog_objs:
            pg_html += '<li><a href = "{_url}" >{_name}</a></li>'.format(_url=obj.link, _name=obj.name)
        return pg_html
    except Exception as e:
        Logger().log(e, True)
        return server_error


def tag_link(self):
    try:
        tag_objs = ArticleType.select()
        pg_html = ""
        for obj in tag_objs:
            pg_html += '<li><a href = "/tag/{_kid}">{_kw}</a></li>'.format(_kid=obj.id, _kw=obj.article_type)
        return pg_html
    except Exception as e:
        Logger().log(e, True)
        return server_error


def last_change_link(self):
    try:
        article_objs = Article.select(Article.id, Article.title).order_by(Article.update_date.desc()).limit(6)
        pg_html = ""
        for obj in article_objs:
            title = obj.title[0:6] + ' ...'
            pg_html += '<li><a href = "/article/{_id}.html" >{_ti}</a></li>'.format(_id=obj.id, _ti=title)
        return pg_html
    except Exception as e:
        Logger().log(e, True)
        return server_error


def hottest_link(self):
    try:
        article_objs = Article.select(Article.id, Article.title).order_by(Article.read_count.desc()).limit(6)
        pg_html = ""
        for obj in article_objs:
            title = obj.title[0:6] + ' ...'
            pg_html += '<li><a href = "/article/{_id}.html" >{_ti}</a></li>'.format(_id=obj.id, _ti=title)
        return pg_html
    except Exception as e:
        Logger().log(e, True)
        return server_error
