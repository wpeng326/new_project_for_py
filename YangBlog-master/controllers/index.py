from tornado.web import RequestHandler
from core.request_handler import BaseHandler
from models.blog import Blog, Article, UserInfo
from utils.log import Logger
from utils.pagination import Page


class IndexHandler(BaseHandler):
    def get(self):
        current_page = self.get_argument("p", 1)
        per_page_count = self.get_argument("pre", 10)
        try:
            current_page = int(current_page)
            per_page_count = int(per_page_count)
        except ValueError as e:
            Logger().log(e, True)
            self.redirect('/index')
        try:
            data_count = Article.select().count()
            page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=per_page_count)
            page_html = page_obj.page_str(base_url="index?")
            at_list = []
            if current_page == 1:
                article_objs = Article.select()[-page_obj.end:]
            else:
                article_objs = Article.select()[-page_obj.end:-page_obj.start]

            for article_obj in article_objs:
                at_list.append({'id': article_obj.id,
                                'title': article_obj.title,
                                'summary': article_obj.summary,
                                'read_count': article_obj.read_count,
                                'created_date': article_obj.created_date,
                                'article_type': article_obj.article_type.article_type
                                })
            at_list.reverse()
        except Exception as e:
            Logger().log(e, True)
            return self.render('index/500.html')
        if current_page == 1 and len(at_list) < per_page_count:
            page_html = ""
        self.render('index/index.html', at_list=at_list, page_html=page_html)


class ArticleHandler(BaseHandler):
    def get(self, article_id=None):
        if article_id:
            try:
                article_obj = Article.get(Article.id == article_id)
                article_data = {'id': article_obj.id,
                                'title': article_obj.title,
                                'content': article_obj.content,
                                'read_count': article_obj.read_count,
                                'created_date': article_obj.created_date,
                                'update_date': article_obj.update_date,
                                'article_type': article_obj.article_type.article_type
                                }
                Article.update(read_count=Article.read_count + 1).where(Article.id == article_id).execute()
                n_article_obj = Article.select(Article.id).where(Article.id > article_id).order_by(Article.id.asc()).limit(1)
                n_a_id = []
                for i in n_article_obj:
                    n_a_id.append(i.id)
                if len(n_a_id) == 1:
                    n_a_id = n_a_id[0]
                else:
                    n_a_id = article_id
                article_data['n_a_id'] = n_a_id
                p_article_obj = Article.select(Article.id).where(Article.id < article_id).order_by(Article.id.desc()).limit(1)
                p_a_id = []
                for i in p_article_obj:
                    p_a_id.append(i.id)
                if len(p_a_id) == 1:
                    p_a_id = p_a_id[0]
                else:
                    p_a_id = article_id
                article_data['p_a_id'] = p_a_id
            except Article.DoesNotExist as e:
                Logger().log(e, True)
                return self.redirect('/404')
            except Exception as e:
                Logger().log(e, True)
                return self.render('index/500.html')
            return self.render('index/article.html', article_data=article_data)
        self.redirect('/404')


class SearchHandler(BaseHandler):
    def get(self):
        title = self.get_argument('title', None)
        current_page = self.get_argument("p", 1)
        per_page_count = self.get_argument("pre", 10)
        try:
            current_page = int(current_page)
            per_page_count = int(per_page_count)
        except ValueError as e:
            Logger().log(e, True)
            self.redirect('/index')
        if title:
            try:
                data_count = Article.select().where(Article.title.contains(title)).count()
                if data_count <= 0:
                    return self.redirect('/404')
                page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=per_page_count)
                page_html = page_obj.page_str(base_url="search?title={_kw}".format(_kw=title))
                search_list = []
                if current_page == 1:
                    search_objs = Article.select().where(Article.title.contains(title))[-page_obj.end:]
                else:
                    search_objs = Article.select().where(Article.title.contains(title))[-page_obj.end:-page_obj.start]
                for search_obj in search_objs:
                    search_list.append({'id': search_obj.id,
                                        'title': search_obj.title,
                                        'summary': search_obj.summary,
                                        'read_count': search_obj.read_count,
                                        'created_date': search_obj.created_date,
                                        'article_type': search_obj.article_type.article_type
                                        })
                search_list.reverse()
                if current_page == 1 and len(search_list) < per_page_count:
                    page_html = ""
                self.render('index/search.html', search_list=search_list, page_html=page_html)
            except Exception as e:
                Logger().log(e, True)
                return self.render('index/500.html')
        self.redirect('/index')


class TagsHandler(BaseHandler):
    def get(self, tag_id=None):
        current_page = self.get_argument("p", 1)
        per_page_count = self.get_argument("pre", 10)
        try:
            current_page = int(current_page)
            per_page_count = int(per_page_count)
        except ValueError as e:
            Logger().log(e, True)
            return self.redirect('/index')
        if tag_id:
            try:
                data_count = Article.select().where(Article.article_type_id == tag_id).count()
                if data_count <= 0:
                    return self.redirect('/404')
                page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=per_page_count)
                page_html = page_obj.page_str(base_url="/tag/{_tid}?".format(_tid=tag_id, ))
                tag_list = []
                if current_page == 1:
                    tag_objs = Article.select().where(Article.article_type_id == tag_id)[-page_obj.end:]
                else:
                    tag_objs = Article.select().where(Article.article_type_id == tag_id)[-page_obj.end:-page_obj.start]
                for search_obj in tag_objs:
                    tag_list.append({'id': search_obj.id,
                                     'title': search_obj.title,
                                     'summary': search_obj.summary,
                                     'read_count': search_obj.read_count,
                                     'created_date': search_obj.created_date,
                                     'article_type': search_obj.article_type.article_type
                                     })
                tag_list.reverse()
                if current_page == 1 and len(tag_list) < per_page_count:
                    page_html = ""
                return self.render('index/tag.html', tag_list=tag_list, page_html=page_html)
            except Exception as e:
                Logger().log(e, True)
                return self.render('index/500.html')
        self.redirect('/index')


class AboutHandler(BaseHandler):
    def get(self):
        try:
            blog_obj = Blog.get(Blog.id == 1)
            user_obj = UserInfo.get(UserInfo.username == 'yang')
            about_data = {'username': user_obj.username,
                          'email': user_obj.email,
                          'about': blog_obj.about}
        except Exception as e:
            Logger().log(e, True)
            return self.render('index/500.html')
        self.render('index/about.html', about_data=about_data)


class NotfindHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.render('index/404.html')


class ServerErrorHandler(RequestHandler):
    def get(self, *args, **kwargs):
        return self.render('index/500.html')