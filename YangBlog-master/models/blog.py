from peewee import *
from playhouse.db_url import connect
import datetime
from config import MYSQL_URL


blog = connect(MYSQL_URL)


class BaseModel(Model):
    class Meta:
        database = blog


class UserInfo(BaseModel):
    username = CharField(unique=True, max_length=50, verbose_name='用户名', null=False)
    password = CharField(max_length=128, verbose_name='密码', null=False)
    nickname = CharField(max_length=50, verbose_name='昵称', default='')
    email = CharField(verbose_name='邮箱', unique=True, null=False)
    avatar = CharField(verbose_name='头像', null=True, default='')
    created_date = DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    update_date = DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)


class Blog(BaseModel):
    title = CharField(verbose_name='个人博客标题', max_length=64)
    site = CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    theme = CharField(verbose_name='博客主题', max_length=32)
    about = CharField(verbose_name='关于我')
    copyright = CharField(verbose_name='底部信息')
    created_date = DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    update_date = DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)


class ArticleType(BaseModel):
    article_type = CharField(verbose_name='文章标签', max_length=128)


class Article(BaseModel):
    title = CharField(verbose_name='文章标题', max_length=128)
    summary = CharField(verbose_name='文章简介', max_length=255)
    read_count = IntegerField(default=0)
    content = TextField(verbose_name='文章内容')
    created_date = DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    update_date = DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)
    article_type = ForeignKeyField(ArticleType)


class FriendlyLink(BaseModel):
    name = CharField(verbose_name='友链名称', max_length=64)
    link = CharField(verbose_name='友链url', max_length=64, unique=True)
    weight = IntegerField(verbose_name='友链权重')
    created_date = DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    update_date = DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)


class UploadFileInfo(BaseModel):
    name = CharField(verbose_name='文件名称', max_length=128)
    key = CharField(verbose_name='对象存储Key', max_length=64)
    hash = CharField(verbose_name='对象存储HASH', max_length=64)
    created_date = DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)


class ServerStatus(BaseModel):
    cpu_load_1 = CharField(max_length=50, verbose_name='1分钟负载', null=True)
    cpu_load_5 = CharField(max_length=50, verbose_name='5分钟负载', null=True)
    cpu_load_15 = CharField(max_length=50, verbose_name='15分钟负载', null=True)
    cpu_iowait = CharField(max_length=50, verbose_name='cpu io', null=True)
    cpu_system = CharField(max_length=50, verbose_name='cpu sys', null=True)
    cpu_idle = CharField(max_length=50, verbose_name='cpu idle', null=True)
    mem = CharField(max_length=50, verbose_name='内存', null=True)
    disk = CharField(max_length=50, verbose_name='硬盘', null=True)
    created_date = DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    update_date = DateTimeField(verbose_name='更新时间', default=datetime.datetime.now)

##########################
def create_tables():
    blog.connect()
    # blog.create_tables([UserInfo, Blog, Article])
    blog.create_tables([ServerStatus])
    blog.close()


def drop_tables():
    blog.connect()
    blog.drop_tables([ServerStatus])
    blog.close()

# drop_tables()
# create_tables()

def create_status():
    obj = ServerStatus()
    obj.cpu_load_1 = '0.05'
    obj.cpu_load_5 = '0.16'
    obj.cpu_load_15 = '0.27'
    obj.save()

# create_status()

# drop_tables()
# create_tables()


def create_test():
    user = UserInfo(username='yang')
    user.password = '123456'
    user.email = 'inboxcvt@gmail.com'
    user.save()


def update_test():
    pass


def delete_test():
    user = UserInfo.get(UserInfo.username == 'yang')
    user.delete_instance()


def select_test():
    obj = UserInfo.get(UserInfo.username == 'yang')
    # or
    # User.select().where((User.username == 'shenyang') | (User.username == 'wang')).first()
    # and
    # User.select().where((User.username == 'shenyang'), (User.password == '123')).first()
    if obj:
        print(obj.username)
    else:
        print('none have')


def select_all():
    ret = UserInfo.select()
    for obj in ret:
        print(obj.username)


def update_test():
    obj = UserInfo.get(UserInfo.username == 'yang')
    obj.password = '123'
    obj.u_time = datetime.datetime.now()
    obj.save()


# update_test()
# create_test()
# delete_test()
# select_test()
# update_test()
# print(datetime.datetime.now())

def create_a(i):
    obj = Article(title='阿里：未经批准不得违规擅自开展4K业务_{_i}'.format(_i=i))
    obj.summary = "近日，国家新闻出版广电总局向各省广电局及相关单位下发了关于规范和促进4K超高清电视发展的通知。通知针对超高清\
    电视发展中出现的管理不规范、技术质量不达标等问题，提出了7条指导性意见：一、充分认识发展4K超高清电视的重要性和艰巨性，坚持从\
    实际出发，加强政策引导。二、优先支持高清电视发展较好的省份和机构开展4K超高清电视试点，坚持试点先行，稳中求进_{_i}".format(_i=i)
    obj.content = '国家新闻出版广电总局文件新广电发[2017]230号'
    obj.article_type = 5
    obj.save()

def delete_a(i):
    user = Article.get(Article.id == i)
    user.delete_instance()

def create_blog():
    obj = Blog(title='YangEver的博客')
    obj.site = '前进前进..'
    obj.about = '关于我'
    obj.copyright = '©2017 prozhi.com 京ICP证030173号 京公网安备11000002000001号'
    obj.theme = 'Black'
    obj.save()

# create_blog()

def create_table():
    blog.connect()
    blog.create_tables([Article, ArticleType])
    blog.close()

def create_at():
    type_choices = [
        (1, "Python"),
        (2, "Linux"),
        (3, "OpenStack"),
        (4, "GoLang"),
        (5, "资讯")
    ]
    for i in type_choices:
        at = ArticleType(article_type=i[1])
        at.save()

def create_fl():
    blog.connect()
    blog.create_tables([FriendlyLink])
    blog.close()

# create_fl()
#

def insert_fl():
    fl_list = [
        {'name': '百度',
         'link': 'http://www.baidu.com',
         'weight': '10'},
        {'name': 'Hao123',
         'link': 'http://www.hao123.com',
         'weight': '11'},
        {'name': '知乎',
         'link': 'http://www.zhihu.com',
         'weight': '12'},
        {'name': '淘宝',
         'link': 'http://www.taobao.com',
         'weight': '13'},
        {'name': 'Web',
         'link': 'http://www.prozhi.com',
         'weight': '5'},
    ]

    for i in fl_list:
        at = FriendlyLink(name=i['name'])
        at.link = i['link']
        at.weight = i['weight']
        at.save()

# blog_objs = FriendlyLink.select().order_by(FriendlyLink.weight)
# for i in blog_objs:
#     print(i.name, i.weight)

# insert_fl()
# create_table()
# create_at()

# for i in range(1, 60):
#     create_a(i)

# print(Article.select().where(Article.title.contains('电')).count())
# print(Article.select().where(Article.title ** ('%电%')).count())

# obj = Article.type_choices
# print(obj)

# at = Article.get(id=2)
# print(at.title)
# print(at.article_type.article_type)
# for a in ArticleType.select():
#     print(a.article_type)
# for i in Article.select().where(Article.article_type.article_type).execute():
# for i in Article.select().join(ArticleType).where(ArticleType.article_type == 'Python').execute():
#     print(i.article_type.article_type)