# coding:utf-8
import json
import re
import sys
import time
import requests
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf8')


# 获取cookie
def Obtain_cookie():
    cookie_url = 'http://47.97.189.210:5001/renrenche'
    response = requests.get(url=cookie_url)
    return response.text


# 主函数
def main():
    for i in range(1, 51):
        print '第{}页'.format(i)
        url = 'https://www.renrenche.com/sh/ershouche/p{}/'.format(i)
        headers = json.loads(Obtain_cookie())
        response = requests.get(url=url, headers=headers)
        html = etree.HTML(response.text)
        detail_url_list = html.xpath('//ul[@class="row-fluid list-row js-car-list"]//li/a/@href')
        for detail_url in detail_url_list:
            time.sleep(0.5)
            detail_url = 'https://www.renrenche.com' + str(detail_url)
            if '/sh/car/' in detail_url:
                parse(detail_url)


# 解析函数
def parse(url):
    item = {}

    print url
    headers = json.loads(Obtain_cookie())
    while True:
        try:
            response = requests.get(url=url, headers=headers, timeout=10)
        except:
            print '超时，重新访问'
            continue
        else:
            break
    print response.status_code
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

    item['url'] = url
    item['name'] = name
    item['price'] = price
    item['Kilometres'] = Kilometres
    item['Card_time'] = Card_time
    item = json.dumps(item, ensure_ascii=False)
    with open('log.txt', 'a+') as f:
        f.write(item+"\n")


if __name__ == '__main__':
    main()

