import re
import csv
import json
import time
import requests
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RecursionError:
        return None


def parse_one_page(html):
    pattern = re.compile('<h3>.*?title="(.*?)".*?</a>'  # 公司名
                         + '.*?<ul.*?company-contact.*?<li.*?addr.*?<span>.*?</span>(.*?)</li>'  # 所在地
                         + '.*?<li.*?telphone.*?<em.*?title="(.*?)".*?</em>'  # 联系电话
                         + '.*?<li.*?person.*?<em.*?title="(.*?)".*?</em>', re.S)  # 联系人
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '公司': item[0],
            '所在地': item[1].strip(),
            '联系电话': item[2],
            '联系人': item[3]
        }


# 写入文件
def write_to_file(content):
    with open('made in China.csv', 'a', newline='', encoding='gbk') as csvfile:
        fieldnames = ['公司', '所在地', '联系电话', '联系人']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(content)


def main(offset):
    url = 'https://jixie.cn.made-in-china.com/qualitysuppliers/all-' + str(offset) + '.html'
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        # 写入
        write_to_file(item)


if __name__ == '__main__':
    # 提取页数
    for i in range(10):
        main(offset=i + 1)
        time.sleep(1)
