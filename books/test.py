#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-06-04 11:34:28
# Project: mafengwo

a="http://222.asdsad.com/asda/asdasd"
b=a.replace("://","")
inx=b.find("/")
print(a[:inx+4])