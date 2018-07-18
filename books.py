#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-06-25 15:25:12
# Project: books

from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysqldb import SQL

class Handler(BaseHandler):
    crawl_config = {
    }
    bookName="天龙八部"
    sql = SQL()
    @every(minutes=1)
    def on_start(self):
        self.crawl('http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd='+self.bookName+" 在线阅读", callback=self.index_page,fetch_type='js',validate_cert = False)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http://www.baidu.com/link?url="]').items():
            self.crawl(each.attr.href, callback=self.detail_page,fetch_type='js',validate_cert = False)
        for each in response.doc('a[href^="http://www.baidu.com/s?"]').items():
            self.crawl(each.attr.href, callback=self.index_page,fetch_type='js',validate_cert = False)

    @config(priority=4)
    def detail_page(self, response):
        a=response.url
        b=a.replace("://","")
        inx=b.find("/")
        host=a[:inx+4]
        if "baidu.com" in host:
            return 
        for each in response.doc('a[href^="'+host+'"]').items():
            self.crawl(each.attr.href, callback=self.find_page,fetch_type='js',validate_cert = False)
        
        result1={
            "url": response.url,
            "title": response.doc('title').text(),
            "html":response.doc('body').html(),
            "bookName":self.bookName,
            "host":host
        }
        
        self.sql.insert('url',**result1)
        return {}
    @config(priority=4)
    def find_page(self, response):
        a=response.url
        b=a.replace("://","")
        inx=b.find("/")
        host=a[:inx+4]
        if "baidu.com" in host:
            return 
        for each in response.doc('a[href^="'+host+'"]').items():
            self.crawl(each.attr.href, callback=self.find_page,fetch_type='js',validate_cert = False)
        result1={
            "url": response.url,
            "title": response.doc('title').text(),
            "html":response.doc('body').html(),
            "bookName":"",
            "host":host
        }

        self.sql.insert('url',**result1)
        return {}
    #根据html代码分析相似性，判断页面为有效目录页的概率，根据高可信度网页生成可信网页列表
    #如果已存在该域名的可信解析式，通过验证则直接判定为可信网页
    
    #根据高可信网页生成各域名下的解析格式
    
    #根据解析式，解析数据
