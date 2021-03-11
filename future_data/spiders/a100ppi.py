import scrapy
from datetime import datetime, date, timedelta
import os
import re
from ..consts import *
import pandas as pd
import numpy as np
from ..items import *
import xml.etree.ElementTree as ET

one_day = timedelta(days=1)
today = datetime.now().date()
upper_case_re = re.compile('[A-Z]')


class A100ppiSpider(scrapy.Spider):
    name = '100ppi'
    allowed_domains = ['cffex.com.cn/']
    base_url = 'file:///Users/marcoyu/Developer/crawler/'
    next_date = date(2020, 1, 1)  # 开始日期
    end_date = date(2021, 2, 11)  # 开始日期
    # end_date = today  # date(2020, 8, 6)

    def next(self):
        """
        计算下一个要采集的链接地址，要存储的文件路径和日期
        如果文件已经存在，则跳过采集，需要重新采集则删除对应文件
        :return:
        """
        nd = self.next_date
        # 最多采集到今天
        if nd >= self.end_date:
            return None, None, None

        # self.logger.info(nd)
        # self.logger.info(nd.day)
        while True:
            path = f'''./{nd.year}/{nd.year}-{nd.month}-{nd.day}.html'''
            exists = os.path.exists(path)
            nd += one_day
            if exists:
                break

        date_str = (nd - one_day).strftime('%Y-%m-%d')
        self.next_date = nd
        # path_date_format = self.next_date.strftime('%Y%m/%d')
        url = f'''{self.base_url}{path[2:]}'''
        # self.logger.info('%s %s %s', url, path, date_str)
        return url, path, date_str

    def start_requests(self):
        url, path, date_str = self.next()
        while url:
            if 'robots' in url:
                continue
            yield scrapy.Request(url=url, callback=self.parse, meta={'path': path, 'date': date_str})
            url, path, date_str = self.next()

    def parse(self, response):
        if response.status != 200:
            return
        self.logger.info('parsing--------')
        path = response.meta.get('path')
        date_str = response.meta.get('date')
        # self.logger.info(response.url)
        # self.logger.info(path)
        # os.makedirs(date_str[0:4], exist_ok=True)
        # with open(path, 'wb') as f:
        #     f.write(response.body)

        # 找到有商品数据的行
        root = ET.fromstring(response.text)
        for data in root.iter('dailydata'):
            # 取出每列
            ins_id = data.find('instrumentid').text
            if ins_id.startswith('IO'):
                # 从列中提取对应数据
                fi = OptionItem()
                fi['DateTime'] = date_str
                fi['Stockid'] = ins_id
                fi['HighPrice'] = data.find('highestprice').text
                fi['LowPrice'] = data.find('lowestprice').text
                fi['OpenPrice'] = data.find('openprice').text
                fi['ClosePrice'] = data.find('closeprice').text

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
