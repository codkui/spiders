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
        # path=path+" "+i.tag
        path=path+" "+i.get("class")
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
def domList(books,domName="a"):
#组合A标签的路径与内容
    Alist=[]
    Atexts={}
    for i in books:
        aTemp=[]
        c=i(domName)
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
    return Atexts,Alist
# print(Alist[3])
# print(Atexts)
def likeNum(Atexts,Alist):

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
                # print(k+"   "+k1+"   "+str(sq))
                Atexts[k]+=Atexts[k1]
                exAlist.append(k1)
            


    #清理异常高的值，默认为页面数的两倍
    for i in Atexts.keys():
        if Atexts[i]>len(Alist)*200:
            exAlist.append(i)
    exAlist=set(exAlist)
    for i in exAlist:
        del Atexts[i]
    return Atexts

#根据链接文字相似度迁移权重至链接，反向计算路径的总权重
def rankPath(Atexts,books,Alist):
    pageText=[]
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
        # print(cc+"  "+pathQ[0][0]+"   "+str(pathQ[0][1]))
        pageText.append([cc,pathQ[0][0],0])

    #根据页面提取数据清洗无效页面

    for n in pageText:
        for i in pageText:
            sq=difflib.SequenceMatcher(None,n[0],i[0]).ratio()
            n[2]+=sq
        n[2]=n[2]/len(pageText)

    pageText=sorted(pageText,key=lambda x:x[2],reverse=True)
    for n in pageText:
        if n[2]/pageText[0][2]>0.75:
            print(n[0])

def rankPathForDemo(Atexts,books,Alist):
    pageText=[]
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
        # print(cc+"  "+pathQ[0][0]+"   "+str(pathQ[0][1]))
        pageText.append([cc,pathQ[0][0],0])

    #根据页面提取数据清洗无效页面
    demoText=""
    for n in Atexts.keys():
        demoText+=n

    for n in pageText:
        
        sq=difflib.SequenceMatcher(None,n[0],demoText).ratio()
        n[2]+=sq
    # n[2]=n[2]/len(pageText)

    # pageText=sorted(pageText,key=lambda x:x[2],reverse=True)
    for n in pageText:
        if n[2]>0.75:
            print(n[0])
Atexts,Alist=domList(books)

allLike=likeNum(Atexts,Alist)

rankPath(allLike,books,Alist)

##以下是内容页获取内容的解析方法
# with open("e:\\code\\spiders\\books\\page\\2.html",encoding="utf-8") as f:
#     p=pq(f.read())
#     p("script").remove()

# texts=[]
# for i in p("div").items():
#     text=i.text()
#     path=dompath(i)
#     paths=path.split(" ")
#     texts.append([path,len(paths),len(paths)*10*len(text),len(text),text])
#     # print(text,len(text))
# texts=sorted(texts,key=lambda x:x[2],reverse=True)
# for i in texts:
#     print(i)

##研究如何从字符串和书名中解析出固定的正则规则，以匹配页面为书籍目录页的可信度
## 并且可以通过该解析式将域名下其他书籍名解析出来

bookname="天龙八部"

# title="天龙八部最新章节列表_天龙八部(易亨贞)小说_天龙八部全文阅读 - 快眼看书"
title="天龙八部最新章节(全本大结局)，天龙八部全文阅读，天龙八部无弹窗，作者：金庸 - 三五中文网"

# btitle="最强军婚：首长，求轻宠！最新章节列表_最强军婚：首长，求轻宠！(小喵妖娆)小说_最强军婚：首长，求轻宠！全文阅读 - 快眼看书"
btitle="莽荒纪最新章节(全本大结局)，莽荒纪全文阅读，莽荒纪无弹窗，作者：我吃西红柿 - 三五中文网"

#根据已知小说名将剩余字符串清理
#根据清理后的字符串生成2-最长长度的子串
# a=title.replace(bookname,"")
a=title.split(bookname)
seChar={}
for i in a:
    for n in range(len(i)-1):
        q=n+2
        for t in range(len(i)-q+1):
            thisChar=i[t:t+q]
            if thisChar in seChar.keys():
                seChar[thisChar]+=1
            else:
                seChar[thisChar]=1
# print(seChar)
#根据未知标题进行重复度验证
for i in seChar:
    if i in btitle:
        seChar[i]+=1
# spilitWord1=sorted(seChar.items(),key=lambda x:x[1],reverse=True)
# print(spilitWord1)
# print(len(seChar.keys()))

#清洗无效数据，包括子字符串，出现1次的字符串
qChar=[]
for i in seChar:
    if seChar[i]==1:
        qChar.append(i)
        continue
    for n in seChar:
        if n in i and n!=i and seChar[n]<=seChar[i]:
            qChar.append(n)

qChar=set(qChar)

# print(qChar)
# print(len(qChar))
newSeChar={}
for i in seChar:
    # print(i)
    if i in qChar:
        pass
    else:
        # print(i)
        newSeChar[i]=seChar[i]

print(newSeChar)

#根据有效截取小说名
newTitile=btitle
for i in newSeChar:
    newTitile=newTitile.replace(i,"####")
newTitile=newTitile.split("####")
print(newTitile)

#根据切分进行可信度计算，第一，重复次数，第二，为子集且不为空
hadTitle={}
for i in newTitile:
    if i=="":
        continue
    if i in hadTitle.keys():
        hadTitle[i]+=1
    else:
        hadTitle[i]=1
    for n in newTitile:
        if i in n and i!=n:
            hadTitle[i]+=1
hadTitle=sorted(hadTitle.items(),key=lambda x:x[1],reverse=True)
print(hadTitle)
# spilitWord={}
# spilitWords={}
# b=title.replace(bookname,"")
# print(b)

# if len(b)==0:
#     print(btitle)    
# else:
#     for i in range(len(b)):
#         spilitWord[b[i]]=True
#     print(spilitWord)

#     temp=""
#     for i in title:
#         if i in spilitWord.keys():
#             temp+=i
#             # spilitWords[temp]=len(temp)
#             spilitWords[temp]=1
#         else:
#             temp=""
#     print(spilitWords)
#     temp=""
#     for i in btitle:
#         if i in spilitWord.keys():
#             temp+=i
#             if temp in spilitWords.keys():
#                 # spilitWords[temp]=spilitWords[temp]*4
#                 spilitWords[temp]+=1
#             else:
#                 # spilitWords[temp]=len(temp)
#                 spilitWords[temp]=1
#         else:
#             temp=""
#     print(spilitWords)
#     #循环迭代，将所有被包含且出现次数等于低于父级的字符串丢弃
#     qChar=[]
#     for i in spilitWords:
#         for n in spilitWords:
#             if n in i and n!=i and spilitWords[n]<=spilitWords[i]:
#                 print(n)
#                 qChar.append(n)
#     qChar=set(qChar)
#     print(qChar)
#     spilitWord1=sorted(spilitWords.items(),key=lambda x:x[1],reverse=True)
#     print(spilitWord1)
#     exit()
    
# b=title.split(bookname)
# print(b)

# if len(b)==0 and b[0]=="":
#     print(btitle)    
# else:
#     bSpi=btitle
#     for i in b:
#         if i=="":
#             continue
#         bSpi=bSpi.replace(i,"$$")
#     print(bSpi)
#     bSpi=bSpi.split("$$")
#     print(bSpi)