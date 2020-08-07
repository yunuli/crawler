import scrapy
from datetime import datetime, date, timedelta
import os
import pandas as pd
import numpy as np
from ..items import *

one_day = timedelta(days=1)
today = datetime.now().date()


class A100ppiSpider(scrapy.Spider):
    name = '100ppi'
    allowed_domains = ['100ppi.com']
    base_url = 'http://www.100ppi.com/sf2/day'
    next_date = date(2010, 1, 1)  # 开始日期
    end_date = today  # date(2020, 8, 6)

    def next(self):
        """
        计算下一个要采集的链接地址，要存储的文件路径和日期
        如果文件已经存在，则跳过采集，需要重新采集则删除对应文件
        :return:
        """
        nd = self.next_date
        # 最多采集到今天
        if nd >= today:
            return None, None, None

        exists = True
        while exists:
            path = f'''./{nd.year}/{nd.year}-{nd.month}-{nd.day}.html'''
            exists = os.path.exists(path)
            if exists:
                nd += one_day

        url = f'''{self.base_url}-{nd.year}-{nd.month}-{nd.day}.html'''
        date_str = self.next_date.strftime('%Y-%m-%d')
        self.next_date = nd + one_day
        self.logger.info('%s %s %s', url, path, date_str)
        return url, path, date_str

    def start_requests(self):
        url, path, date_str = self.next()
        while url:
            yield scrapy.Request(url=url, callback=self.parse, meta={'path': path, 'date': date_str})
            url, path, date_str = self.next()

    def parse(self, response):
        self.logger.info('parsing--------')
        path = response.meta.get('path')
        date_str = response.meta.get('date')
        self.logger.info(response.url)
        self.logger.info(path)
        os.makedirs(date_str[0:4], exist_ok=True)
        with open(path, 'wb') as f:
            f.write(response.body)

        # 找到有商品数据的行
        rows = response.css('#fdata>tr[bgcolor="#fafdff"]')
        for row in rows:
            # 取出每列
            tds = row.css('tr[bgcolor="#fafdff"]>td')
            print(len(tds))
            # 从列中提取对应数据
            results = [''.join(texts).strip() for texts in tds.css('::text').getall()]
            print((results))
            fi = FutureDataItem()
            fi['date'] = date_str
            fi['commodity'] = results[0]
            fi['price'] = results[1]
            fi['code'] = results[2]
            fi['main_price'] = results[3]
            fi['base_diff'] = results[5]
            fi['base_diff_percentage'] = results[6]
            fi['highest_base_diff'] = results[8]
            fi['lowest_base_diff'] = results[9]
            fi['average_base_diff'] = results[10]
            yield fi

    # table = [
    #     [''.join(tds.css('::text').getall()).strip()
    #      for tds in row.css('tr[bgcolor="#fafdff"]>td')]
    #     for row in rows
    # ]
    # df = pd.DataFrame(np.array(table),
    #                   columns=['commodity', 'price', 'code', 'contract_price', 'base_diff', 'highest', 'lowest',
    #                            'average'])
    # dt = response.meta.get('date')
    # df['date'] = np.array([dt] * len(df))
    # self.log(df)
    pass
