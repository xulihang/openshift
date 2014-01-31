# -*- coding: utf-8 -*-  

'''from bottle import route, default_app

@route('/name/<name>')
def nameindex(name='Stranger'):
    return '<strong>Hello, %s!</strong>' % name
 
@route('/')
def index():
    return '<strong>Hello World!</strong>'

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
    'runtime/repo/wsgi/views/')) 

application=default_app()'''
import os
from bottle import route, run, template, request, static_file, default_app, TEMPLATE_PATH
import sqlite3
import json
import urllib

TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
    'app-root/runtime/repo/wsgi/views/')) 

#Hello
@route('/')
def hello():
    return os.getcwd()
  
#登录
@route("/login",method="post")
def login():
    global isbn
    global lasttime
    username = request.forms.get("username");
    password = request.forms.get("password");
    isbn = request.forms.get("isbn");
    lasttime = request.forms.get("time");
    print(username,password,isbn,lasttime)
    exist=1#默认插入
    print exist
    if username =='admin' and password =='admin':
        params = isbn
        f = urllib.urlopen("https://api.douban.com/v2/book/isbn/:"+str(params))
        jresult=f.read()
        jsonVal = json.loads(jresult)
        bookcode=jsonVal["isbn13"]
        #判断是否已经存在
        conn = sqlite3.connect('/var/lib/openshift/52eb84685973ca7f720000b2/app-root/runtime/repo/wsgi/book.db')
        c = conn.cursor()
        for isbncode in c.execute('select code from book'):
            if str("(u'"+bookcode+"',)") == str(isbncode):
                exist=0
        print exist
        if exist==0:
            update()
        else:
            insert()
        

        return username+'登录成功';
    else :
        return username+'登录失败';

#用户登录页面的
@route("/index")
def index():
    
    return template("index")

#下载页面的
@route("/get")
def get():
    
    return static_file("book.db","/var/lib/openshift/52eb84685973ca7f720000b2/app-root/runtime/repo/wsgi",download="book.db")

#插入
def insert():
    params = isbn
    f = urllib.urlopen("https://api.douban.com/v2/book/isbn/:"+str(params))
    jresult=f.read()
    jsonVal = json.loads(jresult)
    bookcode=jsonVal["isbn13"]
    bookname=jsonVal["title"]
    bookprice=jsonVal["price"]
    bookpublisher=jsonVal["publisher"]
    bookpubdate=jsonVal["pubdate"]
    conn = sqlite3.connect('/var/lib/openshift/52eb84685973ca7f720000b2/app-root/runtime/repo/wsgi/book.db')
    c = conn.cursor()
    c.execute("insert into book values ('"+bookname+"','"+bookprice+"','"+bookpublisher+"','"+bookcode+"','"+bookpubdate+"','"+lasttime+"','0')")
    conn.commit()
    c.close()
    conn.close()

#修改
def update():
    #print "Not changed"
    conn = sqlite3.connect('/var/lib/openshift/52eb84685973ca7f720000b2/app-root/runtime/repo/wsgi/book.db')
    c = conn.cursor()
    c.execute("update book set lasttime='"+lasttime+"' where code Like "+isbn+"")
    conn.commit()


def find():
    conn = sqlite3.connect('/var/lib/openshift/52eb84685973ca7f720000b2/app-root/runtime/repo/wsgi/book.db')
    c = conn.cursor()
    for isbncode in c.execute('select code from book'):
        print isbncode

#@route('/hello/:name')
#def index(name='World'):
#    return '<b>Hello %s!</b>' % name


#默认端口  run(host='localhost', port=8080)
#run(host='0.0.0.0', port=8080)
application=default_app()
