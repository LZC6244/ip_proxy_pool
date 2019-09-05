# -*- coding: utf-8 -*-
import psycopg2


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class IpProxiesPipeline(object):
#     """
#         将数据存储到 postgresql 数据库
#
#         2019.9.5 弃用
#         数据库操作由代理池服务器提供的接口进行
#     """
#
#     def __init__(self, pg_db, pg_table, pg_user, pg_passwd, pg_host, pg_port):
#         self.pg_db = pg_db
#         self.pg_table = pg_table
#         self.pg_user = pg_user
#         self.pg_passwd = pg_passwd
#         self.pg_host = pg_host
#         self.pg_port = pg_port
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         """
#             scrapy为访问settings提供的方法
#             从settings.py文件中，取得数据库配置
#         """
#         return cls(
#             pg_db=crawler.settings.get('PG_DB'),
#             pg_table=crawler.settings.get('PG_TABLE'),
#             pg_user=crawler.settings.get('PG_USER'),
#             pg_passwd=crawler.settings.get('PG_PASSWD'),
#             pg_host=crawler.settings.get('PG_HOST'),
#             pg_port=crawler.settings.get('PG_PORT')
#         )
#
#     def open_spider(self, spider):
#         """
#         爬虫一旦开启，就会调用这个方法，连接到数据库
#         """
#         self.conn = psycopg2.connect(database=self.pg_db, user=self.pg_user, password=self.pg_passwd, host=self.pg_host,
#                                      port=self.pg_port)
#         self.cur = self.conn.cursor()
#
#     def close_spider(self, spider):
#         """
#         爬虫一旦关闭，就会调用这个方法，关闭数据库连接
#         """
#         self.cur.close()
#         self.conn.close()
#
#     def process_item(self, item, spider):
#         # 查询SQL语句
#         sql_find = """
#         SELECT	*
#         FROM %s
#         WHERE ip='%s' AND port='%s'
#         """ % (
#             self.pg_table,
#             item['ip'],
#             item['port']
#         )
#         self.cur.execute(sql_find)
#         if self.cur.fetchall():
#             # 存在该代理则更新其信息
#             # 更新SQL语句
#             sql_up = """
#             UPDATE	%s
#             SET anonymity='%s',
#                 net_type='%s',
#                 ip_location='%s',
#                 verify_time='%s'
#             WHERE ip='%s' AND port='%s'
#             """ % (
#                 self.pg_table,
#                 item['anonymity'],
#                 item['net_type'],
#                 item['ip_location'],
#                 item['verify_time'],
#                 item['ip'],
#                 item['port'],
#             )
#             self.cur.execute(sql_up)
#         else:
#             # 不存在则插入该代理信息
#             # 插入SQL语句
#             sql_insert = """
#             INSERT INTO %s
#             (ip,port,anonymity,net_type,ip_location,verify_time)
#             VALUES
#             ('%s','%s','%s','%s','%s','%s')
#             """ % (
#                 self.pg_table,
#                 item['ip'],
#                 item['port'],
#                 item['anonymity'],
#                 item['net_type'],
#                 item['ip_location'],
#                 item['verify_time'],
#             )
#             self.cur.execute(sql_insert)
#         self.conn.commit()
#         print(item)
#         return item
