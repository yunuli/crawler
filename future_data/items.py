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
        '代码': 'code',
        '主力合约价格': 'main_price',
        '基差': 'base_diff',
        '基差百分比': 'base_diff_percentage',
        '180天最高基差': 'highest_base_diff',
        '180天最低基差': 'lowest_base_diff',
        '180天平均基差': 'average_base_diff'
    }
    date = scrapy.Field()
    commodity = scrapy.Field()
    price = scrapy.Field()
    code = scrapy.Field()
    main_price = scrapy.Field()
    base_diff = scrapy.Field()
    base_diff_percentage = scrapy.Field()
    highest_base_diff = scrapy.Field()
    lowest_base_diff = scrapy.Field()
    average_base_diff = scrapy.Field()
    pass
