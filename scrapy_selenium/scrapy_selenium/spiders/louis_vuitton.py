# -*- coding: utf-8 -*-
import json
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy import Request, Spider
from ..items import ScrapySeleniumItem


def process_item_request(request: Request, _):
    wait_until = EC.visibility_of_any_elements_located((By.XPATH, '//div[@class="lv-product-visual"]//img/@srcset'))

    request.meta['wait_time'] = 10
    request.meta['wait_until'] = wait_until
    request.meta['is_selnium_request'] = True
    return request


class LouisVuittonSpider(Spider):
    name = 'louis_vuitton'
    allowed_domains = ['jp.louisvuitton.com']
    start_urls = ['https://jp.louisvuitton.com/jpn-jp/products/brazza-wallet-lv-aerogram-nvprod2630099v']

    def start_requests(self):
        for url in self.start_urls:
            yield process_item_request(
                Request(
                    url=url,
                    callback=self.parse
                ),
                None
            )


    def parse(self, response):
        item = ScrapySeleniumItem()
        item['name'] = response.xpath('//title/text()').get()
        return item
