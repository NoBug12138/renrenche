# coding:utf-8
import json
import re
import sys
import requests
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf8')


url = 'https://www.renrenche.com/sh/car/3380c2401015b292?plog_id=428b259b6be018729841a46bb24d5fef'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}

response = requests.get(url=url, headers=headers)
html = etree.HTML(response.text)

# 获取车辆品牌
try:
    title = html.xpath('//h1/text()')[1]
except:
    title = html.xpath('//h1/text()')[0]
title = re.search('(.*?)-', str(title)).group(1)
print title

# meta标签数据：包含名称，价格，公里数
meta_content = html.xpath('//meta[@name="keywords"]/@content')[0]
# print meta_content
meta_list = str(meta_content).split('，')
# print json.dumps(meta_list, ensure_ascii=False)

# 车辆名称
name = meta_list[5]
if title not in name:
    name = title + '-' + name
print '车辆名称:', name

# 首付价格
price = meta_list[2]
print '价格:', price

# 公里数
Kilometres = meta_list[3]
print '公里数:', Kilometres

# meta标签数据2：包含上牌时间
meta_content_2 = html.xpath('//meta[@name="description"]/@content')[0]
meta_list_2 = str(meta_content_2).split(',')
# print json.dumps(meta_list_2, ensure_ascii=False)
Card_time = re.search('购买时间:(.*)\-', meta_list_2[1]).group(1)
print '上牌时间:', Card_time
