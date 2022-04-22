import scrapy
from scrapy.http import FormRequest
from pprint import pprint
from .. items import HostspiderItem


class Hosts(scrapy.Spider):
    name = 'hosts'
    start_urls = [
        'http://10.20.50.57/zabbix/index.php?request=zabbix.php%3Faction%3Dhost.view%26sort%3Dname%26sortorder%3DASC'
    ]
    hosts_all = []
    ips_all = []
    current_page = 1
    last_page = 0

    def parse(self, response):
        print('\nEntering parse method...')
        title = response.css('title').extract()
        print(title)

        return FormRequest.from_response(response, formdata={
            'name': 'tv-monitor',
            'password': 'monitor1'
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        print('\nEntering start_scraping method...')

        items = HostspiderItem()

        # open_in_browser(response)
        host = response.css('a.link-action::text').extract()
        ip = response.css('td.nowrap::text').extract()

        for h in host:
            self.hosts_all.append(h)
        for i in ip:
            self.ips_all.append(i)

        print(f'------  current_page: {self.current_page}')
        print(f'---------  last_page: {self.last_page}')

        if self.current_page == 1:
            next_page_attr = response.css('nav.paging-btn-container a::attr(aria-label)').extract()
            next_page_attr_last = next_page_attr[-1]
            last_page_num = next_page_attr_last.split(', ')[-1]
            print(f'-- last_page_num: {last_page_num}')
            self.last_page = last_page_num

        if self.current_page == ((int)(self.last_page)):
            items['hosts'] = self.hosts_all
            items['ips'] = self.ips_all
            yield items
        else:
            self.current_page += 1
            next_page_link = 'http://10.20.50.57/zabbix/zabbix.php?action=host.view&page=' + \
                str(self.current_page)
            yield scrapy.Request(url=next_page_link, callback=self.start_scraping)
