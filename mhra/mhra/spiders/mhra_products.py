import scrapy
from bs4 import BeautifulSoup
from scrapy_playwright.page import PageCoroutine
import pandas as pd


class MhraProductsSpider(scrapy.Spider):
    name = 'mhra_products'
    allowed_domains = ['products.mhra.gov.uk']
    start_urls = ['https://products.mhra.gov.uk/substance-index/?letter=A']
    url_prefix = 'https://products.mhra.gov.uk'
    output_df = pd.DataFrame()

    def parse(self, response):
        yield scrapy.Request(url='https://products.mhra.gov.uk/substance-index/?letter=A',
                callback=self.parse_substances, meta={"playwright": True})

    def parse_substances(self, response):
        html_string = response.text
        soup = BeautifulSoup(html_string, 'lxml')
        substances = soup.find_all("li", {"class": "substance-name"})
        for substance in substances[0:1]:
            yield scrapy.Request(url=self.url_prefix+substance.find('a')['href'],
                                 callback=self.parse_product_alias, meta={"playwright": True},
                                 cb_kwargs={'subs': substance.text})

    def parse_product_alias(self, response, subs):
        html_string = response.text
        soup = BeautifulSoup(html_string, 'lxml')
        main_products = soup.find_all("li", {"class": "product-name"})
        for main_product in main_products:
            yield scrapy.Request(url=self.url_prefix + main_product.find('a')['href'],
                                 callback=self.accept_disclaimer,
                                 meta={"playwright": True, "playwright_page_coroutines":[
                                     PageCoroutine("click", selector='xpath=//*[@id="agree-checkbox"]'),
                                     PageCoroutine("click", selector='xpath=//*[@id="__next"]/div/main/div/div'
                                                                     '/section/div/form/button'),
                                 ]},
                                 cb_kwargs={'subs': subs, 'prod': main_product.text})

    def accept_disclaimer(self, response, subs, prod):
        html_string = response.text
        soup = BeautifulSoup(html_string, 'lxml')
        pil_elems = soup.find_all('a', {'class': 'doc-type-pil'})
        spc_elems = soup.find_all('a', {'class': 'doc-type-spc'})

        pil_links = []
        spc_links = []
        for pil_elem in pil_elems:
            pil_links.append(pil_elem['href'])

        for spc_elem in spc_elems:
            spc_links.append(spc_elem['href'])

        yield {'subs': subs, 'prod': prod, 'pil': pil_links, 'spc': spc_links}


