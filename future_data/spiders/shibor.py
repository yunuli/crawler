from datetime import datetime, timedelta
import re
from ..items import *

one_day = timedelta(days=1)
today = datetime.now().date()
upper_case_re = re.compile('[A-Z]')


class A100ppiSpider(scrapy.Spider):
    name = 'shibor'
    allowed_domains = ['shibor.org/']

    def start_requests(self):
        url = 'http://www.shibor.org/shibor/web/html/shibor.html'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info('parsing--------')
        if response.status != 200:
            return
        trs = response.css('tr')
        rows = [tr.css('td').css('::text').getall() for tr in trs]
        self.logger.info(rows)

        si = ShiborItem()
        si['DateTime'] = rows[1][0].strip()
        si['TON'] = rows[5][1]
        si['T1W'] = rows[6][1]
        si['T2W'] = rows[7][1]
        si['T1M'] = rows[8][1]
        si['T3M'] = rows[9][1]
        si['T6M'] = rows[10][1]
        si['T9M'] = rows[11][1]
        si['T1Y'] = rows[12][1]
        print(si)
        yield si
