# coding=utf-8
# encode=utf-8
import requests
from requests.exceptions import RequestException
from config import *
import re
import json
from multiprocessing import Pool
import pymongo
import sys
#解决编码问题
reload(sys)
sys.setdefaultencoding('utf-8')
# 创建mangodb的数据库连接
client = pymongo.MongoClient('localhost', 27017)
# 指定数据库
db = client['Maoyan']
# 指定存放数据的数据库表名称
collection = db['maoyanmovie']
#请求头
HEADERS = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

def get_one_page(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    # with open('body.html', 'w') as f:
    #     f.write(html)
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def write_to_mongo(item):
    # item = dict(item)
    db.movies.save(item)
#
#
def write_to_file(content):
    # a 表示往后追加
    with open('result.txt', 'a') as f:
        f.write(json.dumps(content, ensure_ascii=False) + ',\n')
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)
        # print(item)
        # write_to_mongo(item)


if __name__ == '__main__':
    # pool = Pool()
    # pool.map(main, [i*10 for i in range(10)])
    for i in range(10):
        main(i * 10)



