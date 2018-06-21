import requests
import re
from requests.exceptions import RequestException
def get_one_page(url):
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
    try:
       response=requests.get(url,headers=headers)
       #response.raise_for_status()
       if response.status_code==200:
          return response.text
       return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                       +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items=re.findall(pattern,html)
    #print(items)
    for item in items:
        yield {
            '电影编号':item[0],
            '图片链接':item[1],
            '电影名称':item[2],
            '主演':item[3].strip()[3:],
            '上映时间':item[4].strip()[5:],
            '评分':item[5]+item[6],
        }

def write_to_files(content):
    with open('result.txt','a') as f:
        f.write(json.dumps(content)+'\n')
        f.close()


def main():
    url='http://maoyan.com/board/4'
    html=get_one_page(url)
    #print(html)
    for item in parse_one_page(html):
        print(item)

if __name__=='__main__':
    main()

