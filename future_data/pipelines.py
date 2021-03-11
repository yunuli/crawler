# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sqlalchemy import create_engine, Table, MetaData
import pyodbc

class FutureDataPipeline:
    def process_item(self, item, spider):
        print(item)
        ins = self.table.insert().values(dict(item))
        self.db_engine.execute(ins)
        return item

    def open_spider(self, spider):
        db_host = '172.16.0.10'
        db_user = 'FutureTrade'
        db_pwd = '^8/}Tu@Bqm'
        database_name = 'EXTDB'
        db_link = f'''mssql+pyodbc://{db_user}:{db_pwd}@{db_host}/{database_name}?driver=SQL+Server'''
        db_engine = create_engine(db_link, encoding='utf8')
        metadata = MetaData(bind=None)
        table = Table(
            'tb_SHIBOR_day',
            metadata,
            autoload=True,
            autoload_with=db_engine
        )
        self.db_engine = db_engine
        self.table = table
        pass

    def close_spider(self, spider):
        self.db_engine.close()
        pass
