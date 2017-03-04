# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from qiantu_spider.items import QiantuSpiderItem



class QiantuSpider(scrapy.Spider):
    name = "qiantu"
    allowed_domains = ["58pic.com"]
    start_urls = ['http://58pic.com/']

    def parse(self, response):
        all_url = response.xpath('//div[@class="moren-content"]/a/@href').extract()

        #print(all_url)
        for i in range(0,int(len(all_url))):
            single_url = all_url[i]
            each_html = single_url + '0/day-1.html'  # 将每个页面构造成第一页的网址，方便提取每页的最大页数
            yield Request(each_html,callback=self.list_page,meta={'front':single_url})#把每个子网站传到下面的函数

    def list_page(self,response):
        front_url = response.meta['front']
        try:
            max_page = response.xpath('//*[@id="showpage"]/a[8]/text()').extract()[0]#提取最大页数
            print(max_page)
            #print(front_url)
            try:
                for i in range(1,int(max_page)+1):
                    img_page = front_url+'0/day-'+str(i)+'.html'#构造出每一个分类的所有url，接下来就是提取图片地址了
                    #print(img_page)
                    yield Request(url=img_page,callback=self.get_img_link)
            except:
                print('该网页没有数据')
        except Exception as  e:
            print('网页没有最大页数，作废网页')


    def get_img_link(self,response):
        item =QiantuSpiderItem()
        img_link1 = response.xpath("//a[@class='thumb-box']/img/@src").extract()
        if img_link1:
        #该网站图片有点奇葩，有些页面的图片存储方式不一样，总体来说是这两者，分开写就好了
            item['img_urls'] =img_link1
            #print(1,img_link1)
            yield item
        else:
            img_link2=response.xpath('//*[@id="main"]/div/div/div/div/div/a/img/@src').extract()
            item['img_urls'] = img_link2
            yield item
            #print(2,img_link2)

