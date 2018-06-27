# coding=utf-8
import requests
import json
import re
from requests.exceptions import RequestException
from multiprocessing import Pool

def get_one_pages(url):
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
    try:
        res=requests.get(url,headers=headers)
        res.raise_for_status()
        res.encoding=res.apparent_encoding
        return res.text
    except RequestException:
        return None

def parse_one_page(html):
     pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
     +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
     items=re.findall(pattern,str(html))
     #print(items)
     for item in items:
        #print(type(item))
        #print(item)
        yield {
            '序号：':item[0],
            '图片链接':item[1],
            '名称':item[2],
            '主演':item[3].strip()[3:],
            '上映时间':item[4][5:],
            '评分':item[5]+item[6],
        }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)
    html=get_one_pages(url)
    #print(html)
    parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__=="__main__":
    # for i in range(10):
    #    main(i*10)
    pool=Pool()
    pool.map(main,[i*10 for i in range(10)])
    pool.close()
    pool.join()



