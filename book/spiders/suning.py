# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 大分类分组 小说，散文随笔 -> 中国当代小说 中国近代小说 三个级别
        p_list = response.xpath("//div[@class='menu-sub' or @class='menu-sub menu-sub-down']/div[@class='submenu-left']/p")  # 小说 青春文学
        for p in p_list:
            item = dict()
            item["b_cate"] = p.xpath("./a/text()").extract_first()  # 小说
            # 小分类分组
            li_list = p.xpath("./following-sibling::ul[1]/li")
            for li in li_list:
                item["s_cate"] = li.xpath("./a/text()").extract_first()
                item["s_href"] = li.xpath("./a/@href").extract_first()

                if item["s_href"] is not None:
                    yield scrapy.Request(
                        item["s_href"],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):
        item = deepcopy(response.meta["item"])
        # 图书列表页分组
        li_list = response.xpath("//div[@id='filter-results']/ul/li")
        for li in li_list:
            item["book_img"] = "https:" + li.xpath(".//img/@src2").extract_first()  # book_press 出版社
            item["book_title"] = li.xpath(".//p[@class='sell-point']/a/text()").extract_first()
            item["book_title"] = re.sub(r'\n', '', item["book_title"])
            item["book_store"] = li.xpath(".//p[last()]/a/text()").extract_first()
            item["book_href"] = "https:" + li.xpath(".//div[@class='img-block']/a/@href").extract_first()

            yield scrapy.Request(
                item["book_href"],
                callback=self.parse_book_detail,
                meta={"item":deepcopy(item)}
            )

            # 翻页
            page_count = int(re.findall(r'param.pageNumbers = "(.*?)"', response.body.decode())[0])
            current_page = int(re.findall(r'param.currentPage = "(.*?)"', response.body.decode())[0]) + 1

            # 构建url模板
            cu_url = response.request.url
            t = cu_url.split("-")
            t[2] = "{}"
            url_temp = "-".join(t)

            if current_page < page_count:
                next_url = url_temp.format(current_page)  # 下一页的url
                yield scrapy.Request(
                    next_url,
                    callback=self.parse_book_list,
                    meta={"item":response.meta["item"]}
                )



    def parse_book_detail(self, response):
        item = response.meta["item"]
        item["book_author"] = response.xpath("//li[@class='pb-item'][1]/text()").extract_first()
        item["book_author"] = item["book_author"].strip() if item["book_author"] is not None else None
        item["book_author"] = re.sub(r'[\r,\t,\n]', '', item["book_author"])
        item["book_press"] = response.xpath("//li[@class='pb-item'][2]/text()").extract_first()
        item["book_press"] = item["book_press"].strip() if item["book_press"] is not None else None
        item["book_publish_date"] = response.xpath("//li[@class='pb-item'][3]/span[2]/text()").extract_first()
        item["book_publish_date"] = item["book_publish_date"].strip() if item["book_publish_date"] is not None else None
        item["book_price"] = re.findall(r'"itemPrice":"(.*?)"', response.body.decode())
        item["book_price"] = "￥" + item["book_price"][0] if len(item["book_price"])>0 else None
        yield item
