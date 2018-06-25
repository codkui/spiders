#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-06-04 11:34:28
# Project: mafengwo

from PIL import Image
import os

#图片压缩批处理  
def compressImage(srcPath,dstPath):  
    for filename in os.listdir(srcPath):  
        #如果不存在目的目录则创建一个，保持层级结构
        if not os.path.exists(dstPath):
                os.makedirs(dstPath)        

        #拼接完整的文件或文件夹路径
        srcFile=os.path.join(srcPath,filename)
        dstFile=os.path.join(dstPath,filename)
        print (srcFile)
        print (dstFile)

        #如果是文件就处理
        if os.path.isfile(srcFile):     
            #打开原图片缩小后保存，可以用if srcFile.endswith(".jpg")或者split，splitext等函数等针对特定文件压缩
            if srcFile.endswith(".jpeg")==False:
                continue
            sImg=Image.open(srcFile)  
            w,h=sImg.size
            starH=int((h-383)/2)
            box = (0, starH, 680, 383+starH)
            region = sImg.crop(box) 
            print (w,h)
            print(0,starH)
            #dImg=region.resize((680,383),Image.ANTIALIAS)  #设置压缩尺寸和选项，注意尺寸要用括号
            region.save(dstFile) #也可以用srcFile原路径保存,或者更改后缀保存，save这个函数后面可以加压缩编码选项JPEG之类的
            print (dstFile+" compressed succeeded")

        #如果是文件夹就递归
        if os.path.isdir(srcFile):
            compressImage(srcFile,dstFile)

if __name__=='__main__':  
    compressImage("e:/file/images","e:/file/imagesOk")