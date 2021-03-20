from datetime import datetime
from ..items import *


class A100ppiSpider(scrapy.Spider):
    name = 'shibor'
    allowed_domains = ['shibor.org/']

    def start_requests(self):
        today = datetime.now().date()
        date_str = today.strftime('%Y-%m-%d')
        url = f'''http://www.shibor.org/shibor/Shibor.do?date={date_str}'''
        # url = 'http://www.shibor.org/shibor/web/html/shibor.html'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('parsing--------')
        if response.status != 200:
            return
        si = ShiborItem()

        si['DateTime'] = response.css('tr:first-child td::text').get().strip()

        trs = response.css('.shiborquxian tr')
        rows = [tr.css('td').css('::text').getall() for tr in trs]

        si['TON'] = rows[0][1]
        si['T1W'] = rows[1][1]
        si['T2W'] = rows[2][1]
        si['T1M'] = rows[3][1]
        si['T3M'] = rows[4][1]
        si['T6M'] = rows[5][1]
        si['T9M'] = rows[6][1]
        si['T1Y'] = rows[7][1]
        yield si
