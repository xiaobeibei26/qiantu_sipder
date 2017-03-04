# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.request
import re
import os
class QiantuSpiderPipeline(object):
    def process_item(self, item, spider):
        for url in item['img_urls']:
            try:
                real_url = re.sub(r'!(.*)','',url)#把每个图片地址！号后面的字符去掉，剩下的是高清图地址
                name = real_url[-24:].replace('/','')#去除不能表示文件名的符号，这里将我搞死了

                #print(name)
                file ='E://qiantu/'


                urllib.request.urlretrieve(real_url,filename=file+name)

            except Exception as e:
                print(e,'该图片没有高清地址')
        print('成功下载一页图片')

