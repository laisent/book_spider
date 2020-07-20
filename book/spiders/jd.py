# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath("//div[@class='mc']/dl/dt") # 大分类列表
        for dt in dt_list:
            item = dict()
            item["big_cate"] = dt.xpath("./a/text()").extract_first()  # 大分类名字
            em_list = dt.xpath("./following-sibling::dd[1]/em")  # 小分类列表
            for em in em_list:
                item["small_cate_href"] = em.xpath("./a/@href").extract_first()
                item["small_cate"] = em.xpath("./a/text()").extract_first()  # 小分类名字

                if item["small_cate_href"] is not None:
                    item["small_cate_href"] = "https:" + item["small_cate_href"]
                    yield scrapy.Request(
                        item["small_cate_href"],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)},
                        dont_filter=True
                    )


    """解析各个分类的列表页
    """
    def parse_book_list(self, response):
        item = response.meta["item"]
        li_list = response.xpath("//div[@id='J_goodsList']/ul/li")
        for li in li_list:
            item["book_name"] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first()
            item["book_img"] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            item["book_img"] = "https:" + item["book_img"] if item["book_img"] is not None else None
            item["book_img"] = "https:" + li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            item["book_author"] = li.xpath(".//span[@class='p-bi-name']/a/text()").extract()
            item["book_publish_store"] = li.xpath(".//span[@class='p-bi-store']/a/@title").extract_first()
            item["book_publish_date"] = li.xpath(".//span[@class='p-bi-date']/text()").extract_first()
            item["book_publish_date"] = item["book_publish_date"].strip() if item["book_publish_date"] is not None else None
            item["book_price"] = li.xpath(".//div[@class='p-price']/strong/i/text()").extract_first()
            print(item)

        # 列表页翻页
        # 构造下一页地址
        page_now = int(response.xpath('//div[@id="J_topPage"]/span/b/text()').extract_first())  # 当前页
        page_max = int(response.xpath('//div[@id="J_topPage"]/span/i/text()').extract_first())  # 最大页

        if page_now != 1:
            print("当前页数是{}".format(page_now))

        if page_now < page_max:
            next_page = page_now + 1
            next_url = item["small_cate_href"] + "?page={}".format(2 * next_page - 1)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item": deepcopy(item)}
            )


