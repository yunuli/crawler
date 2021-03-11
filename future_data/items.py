# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FutureDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nameToField = {

        '日期': 'date',
        '商品': 'commodity',
        '现货价格': 'price',
        '合约日期': 'contract_date',
        '主力合约价格': 'main_price',
        '基差': 'base_diff',
        '基差百分比': 'base_diff_percentage',
        '180天最高基差': 'highest_base_diff',
        '180天最低基差': 'lowest_base_diff',
        '180天平均基差': 'average_base_diff',
        '代码': 'code'
    }
    date = scrapy.Field()
    commodity = scrapy.Field()
    price = scrapy.Field()
    contract_date = scrapy.Field()
    main_price = scrapy.Field()
    base_diff = scrapy.Field()
    base_diff_percentage = scrapy.Field()
    highest_base_diff = scrapy.Field()
    lowest_base_diff = scrapy.Field()
    average_base_diff = scrapy.Field()
    code = scrapy.Field()
    pass


class OptionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nameToField = {

        '日期': 'DateTime',
        '商品': 'Stockid',
        '最高': 'HighPrice',
        '最低': 'LowPrice',
        '收盘': 'ClosePrice',
        '开盘': 'OpenPrice',
    }
    DateTime = scrapy.Field()
    Stockid = scrapy.Field()
    HighPrice = scrapy.Field()
    LowPrice = scrapy.Field()
    ClosePrice = scrapy.Field()
    OpenPrice = scrapy.Field()
    pass


class ShiborItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nameToField = {

        '日期': 'DateTime',
        'ON': 'TON',
        '一周': 'T1W',
        '两周': 'T2W',
        '一个月': 'T1M',
        '三个月': 'T3M',
        '六个月': 'T6M',
        '九个月': 'T9M',
        '一年': 'T1Y',
    }
    DateTime = scrapy.Field()
    TON = scrapy.Field()
    T1W = scrapy.Field()
    T2W = scrapy.Field()
    T1M = scrapy.Field()
    T3M = scrapy.Field()
    T6M = scrapy.Field()
    T9M = scrapy.Field()
    T1Y = scrapy.Field()
    pass
