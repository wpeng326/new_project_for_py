# YangBlog
* Tornado Blog

## Demo 地址
[YangBlog](http://demo.blog.izhihu.me)

## 技术栈
* 基于 Py3 + Tornado
* 前端框架 Bootstrap + JQuery
* 富文本编辑框 bootstrap-wysiwyg
* 字体图标 Font Awesome 
* 按钮 Buttons
* 数据库 Mysql + Peewee
* 图片存储  QiniuYun 对象存储
* 前端使用 Chart.js 展示图

## 实现功能
* /index 首页 文章列表，分页展示
* /article 文章页，上一页，下一页按钮
* /search 搜索标题展示页面，分页展示
* 头部标题、底部信息、右侧友链使用ui_methods功能实现
* /admin/index 后端管理页面，实现文章增加，删除，更
* /admin/login 登录，使用Tornado的secure_cookie 认证
* /upload 上传图片处理，直接上传到Qiniu对象存储中

## 待完成
* ~~管理界面中的友链添加，删除，调整权重~~
* ~~管理界面中的最新文章展示~~
* ~~管理界面中的最后更改文章展示~~
* ~~管理界面的Tag分类显示，搜索~~
* 管理员忘记密码重置

## 更新 20171206
* /admin/index 管理页面主页，展示服务器状态，目前仅Linux可用，
* /admin/article 由原来的index迁移到此路由，管理文章
* /admin/tag 管理tag
* /admin/profile 管理个人资料
* /admin/blog 管理博客的基本设置
* /admin/flink 管理友链设置
* /admin/api/v1/status 获取服务器状态，前端Ajax 定时轮训此地址获取最新数据，目前为半分钟一次
* 先完成这些吧，暂时不会经常更新了

## 感谢
* 开源软件
* Qiniu云的免费对象存储

## 使用模块
* peewee
* qiniu

## 部署方法
* config.py 中填写自己的qiniu对象存储的ACCESS_KEY，SECRET_KEY，BUCKET_NAME，BASE_STATIC_URL
* config.py 中修改MYSQL_URL 为自己的地址
* 使用 python app.py 启动，建议使用supervisor 管理程序运行
* 出图需要安装服务器端的脚本，定时任务cron去上报数据到数据库中，不使用的话就把那段逻辑删除即可，不影响其他功能
* 脚本如下
```#!/usr/bin/env python3
import pymysql.cursors
import datetime
import random
import subprocess

config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'',
          'db':'blog',
          'charset':'utf8',
          'cursorclass':pymysql.cursors.DictCursor,
          }

def inster_data(status_data):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = 'INSERT INTO serverstatus (cpu_load_1, cpu_load_5, cpu_load_15, mem, created_date, update_date) VALUES (%s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (status_data['cpu'][0], status_data['cpu'][1], status_data['cpu'][2], status_data['mem'], datetime.datetime.now(), datetime.datetime.now()));
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            connection.commit()
    finally:
        connection.close()

ret = subprocess.check_output("uptime |awk -F 'average:' '{print $2}'",shell=True)
ret = ret.decode('utf-8').replace(' ', '').strip('\n')
cpu_status_data = ret.split(',')
ret = subprocess.check_output("free -m|awk '/Mem/{print $NF}'",shell=True)
ret = ret.decode('utf-8').replace(' ', '').strip('\n')
mem_status_data = ret
save_status = {'cpu':cpu_status_data,'mem': mem_status_data}
#print(save_status)
inster_data(save_status)
```

## 效果图
* index
![index](https://github.com/lgphone/YangBlog/blob/master/doc/pic/index.png)
* article
![article](https://github.com/lgphone/YangBlog/blob/master/doc/pic/article.png)
* search
![search](https://github.com/lgphone/YangBlog/blob/master/doc/pic/search.png)
* about
![about](https://github.com/lgphone/YangBlog/blob/master/doc/pic/about.png)
* page
![page](https://github.com/lgphone/YangBlog/blob/master/doc/pic/page.png)
* admin article
![admin article](https://github.com/lgphone/YangBlog/blob/master/doc/pic/admin_article.png)
* add article
![add article](https://github.com/lgphone/YangBlog/blob/master/doc/pic/article_add.png)
* del article
![del article](https://github.com/lgphone/YangBlog/blob/master/doc/pic/article_del.png)
* edit article
![edit article](https://github.com/lgphone/YangBlog/blob/master/doc/pic/article_edit.png)
* status 
![status ](https://github.com/lgphone/YangBlog/blob/master/doc/pic/status.png)
* admin tag
![admin tag](https://github.com/lgphone/YangBlog/blob/master/doc/pic/admin_tag.png)
* admin flink
![admin flink](https://github.com/lgphone/YangBlog/blob/master/doc/pic/admin_flink.png)
* admin blog
![admin blog](https://github.com/lgphone/YangBlog/blob/master/doc/pic/admin_blog.png)
* admin profile
![admin profile](https://github.com/lgphone/YangBlog/blob/master/doc/pic/admin_profile.png)
