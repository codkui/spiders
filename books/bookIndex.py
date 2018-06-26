#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-06-04 11:34:28
# Project: mafengwo

from pyquery  import PyQuery as pq
import os
import re
import difflib


def dompath(el):
    path=""
    pa=el.parents()
    for i in pa:
        path=path+" "+i.tag
    path+=" "+el[0].tag
    return path
FILEPATH="e:\\code\\spiders\\books\\file\\"
books=[]
for a in os.listdir(FILEPATH):
    with open(FILEPATH+a,encoding="utf-8") as f:
        p=pq(f.read())
        p("script").remove()
        books.append(p)
# print("ccccccccc")
# print(books[0]("div").text())
# print(dompath(books[3]("a").eq(0)))
#组合A标签的路径与内容
Alist=[]
Atexts={}
for i in books:
    aTemp=[]
    c=i("a")
    for n in c.items():
        indexTitle=n.text()
        if indexTitle!="":
            indexTitle=indexTitle.replace("\u3000","")
            indexTitle=indexTitle.replace(" ","")
            if indexTitle in Atexts.keys():
                Atexts[indexTitle]+=200
            else:
                Atexts[indexTitle]=100
            aTemp.append([indexTitle,dompath(n),0])
    Alist.append(aTemp)

# print(Alist[3])
# print(Atexts)
exAlist=[]
#相似度比较坍缩
# difflib.SequenceMatcher
for k in Atexts.keys():
    if k in exAlist:
        continue
    for k1 in Atexts.keys():
        if k1==k or k1 in exAlist:
            continue
        sq=difflib.SequenceMatcher(None,k1,k).ratio()
        
        if sq>0.75:
            print(k+"   "+k1+"   "+str(sq))
            Atexts[k]+=Atexts[k1]
            exAlist.append(k1)
        


#清理异常高的值，默认为页面数的两倍
for i in Atexts.keys():
    if Atexts[i]>len(Alist)*200:
        exAlist.append(i)
exAlist=set(exAlist)
for i in exAlist:
    del Atexts[i]
print(Atexts)

#根据链接文字相似度迁移权重至链接，反向计算路径的总权重
for i in range(len(Alist)):
    for n in Alist[i]:
        #遍历已有总权重，根据相似度迁移权重
        for a in Atexts.keys():
            sq=difflib.SequenceMatcher(None,a,n[0]).ratio()
            if sq>0.75:
                n[2]+=Atexts[a]
                # break
    pathQ={}
    for n in Alist[i]:
        if n[1] in pathQ:
            pathQ[n[1]]+=n[2]
        else:
            pathQ[n[1]]=n[2]
    # print(pathQ)
    pathQ=sorted(pathQ.items(), key=lambda x: x[1], reverse=True)
    # for n in pathQ.keys():
    cc=books[i](pathQ[0][0]).text()
    print(cc+"  "+pathQ[0][0]+"   "+str(pathQ[0][1]))



