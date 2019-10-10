#!/usr/bin/env python3
import tornado.ioloop
import tornado.web
from controllers import index
from controllers import admin
from controllers import uimethods as umt

settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret': '43809138f51b96f8ac24e79b3a2cb482',
    'login_url': '/admin/login',
    'xsrf_cookies': True,
    'debug': True,
    'autoreload': True,
    'ui_methods': umt,
}

application = tornado.web.Application([
    # 主页
    (r"/index", index.IndexHandler),
    # 文章页
    (r"/article/([\d]+).html", index.ArticleHandler),
    # 查询
    (r"/search", index.SearchHandler),
    # 关于
    (r"/about", index.AboutHandler),
    # 登录
    (r"/admin/login", admin.LoginHandler),
    # Dashboard
    (r"/admin/index", admin.IndexHandler),
    # Dashboard
    (r"/admin/article", admin.ArticleHandler),
    # Tag 管理
    (r"/admin/tag", admin.TagsHandler),
    # 个人资料管理
    (r"/admin/profile", admin.ProfileHandler),
    # 网站资料管理
    (r"/admin/blog", admin.BlogHandler),
    # 友链管理
    (r"/admin/flink", admin.FlinkHandler),
    # 登出
    (r"/admin/logout", admin.LogoutHandler),
    # 出状态图
    (r"/admin/api/v1/status", admin.StatusApiHandler),
    # 上传图片
    (r"/upload", admin.UploadHandler),
    # 文章页
    (r"/tag/([\d]+)", index.TagsHandler),
    # 404处理页面
    (r"/404", index.NotfindHandler),
    # 500处理页面
    (r"/500", index.ServerErrorHandler),
    (r".*", index.NotfindHandler),
], **settings)

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
