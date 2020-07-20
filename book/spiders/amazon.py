# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from urllib.parse import unquote


class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b?ie=UTF8&node=658390051']
    redis_key = "amazon"

    rules = (
        # 匹配大分类的url和小分类的url地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='a-row a-expander-container a-expander-extend-container']/li",)), follow=True),
        # 匹配图书的url地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='mainResults']/ul/li//h2/..",)), callback="parse_book_detail"),
        # 列表页翻页
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='pagn']",)), follow=True),
    )

    def parse_book_detail(self, response):
        item = {}
        item["book_url"] = response.url  # 书本url
        item["book_title"] = response.xpath("//span[@id='productTitle']/text()").extract_first().strip()  # 图书标题
        item["book_author"] = response.xpath("//span[@class='author notFaded']/a/text()").extract()  # 图书作者
        item["book_img"] = response.xpath("//div[@id='ebooks-img-canvas']/img/@src").extract_first()  # 图书图片

        item["book_price"] = response.xpath("//span[@class='a-size-base a-color-price a-color-price']/text()").extract_first()  # 图书价格
        if item["book_price"] is None:
            item["book_price"] = response.xpath("//span[@class='a-color-price']/text()").extract_first()
        item["book_price"] = item["book_price"].strip()

        item["book_cate"] = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']/ul/li[not(@class)]/span/a/text()").extract()  # 图书分类
        item["book_cate"] = [i.strip() for i in item["book_cate"]]  # 图书分类

        item["book_publish_store"] = response.xpath("//b[text()='出版社:']/../text()").extract_first()  # 图书出版社

        book_desc_encode = re.findall(r'bookDescEncodedData = "([\S]*)"', response.body.decode())[0] # 正则取出加密字段
        book_desc_decode = unquote(book_desc_encode)  # url解密
        # 方法1：手动解码
        desc_list = re.findall(r'&#x([\S]*?);', book_desc_decode)  # 取出解密后中 C# 加密的部分
        temp_list = list()
        for desc in desc_list:
            # TODO: 解密 C# 算法  格式: &#xXXXX;
            # 1.取出头尾【&#】和【;】
            # 2.中间的字符是ASCII，字符串转换成十六进制的整形 ASCII -> str
            # 3.添加到列表中
            cu_str = chr(int(desc, 16))
            temp_list.append(cu_str)
        book_desc_str = "".join(temp_list)
        """
        方法2：html解码
        import html
        
        # TODO: 先url解码 再html解密
        book_desc_encode = re.findall(r'bookDescEncodedData = "([\S]*)"', response.body.decode())[0] # 正则取出加密字段
        book_desc_decode = unquote(book_desc_encode)  # url解密
        book_desc_str = html.unescape(book_desc_decode)  # html解密
        但是这个解密后仍然有许多<></>的标签 如
            # \n<h3><b><font color="#E47911">内容简介：</font></b></h3>“如果一生只看一本书，一定是《百年孤独》；
            # 如果书架上 只放一本书，一定是《百年孤独》；一千年后还可能流传的“老故事”，一定是《百年孤独》。<br />
        所以这里使用方法1
        """
        item["book_desc"] =book_desc_str  # 图书简洁
        print(item)

