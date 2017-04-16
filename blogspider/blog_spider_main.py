import jieba.analyse
from bs4 import BeautifulSoup
import requests
import re

url = 'http://blog.csdn.net/forezp'

titles=set()

def download(url):
    if url is None:
        return None
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        })
        if (response.status_code == 200):
            return response.content
        return None
    except:
        return None

def parse_title(html):
    if html is None:
        return None
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all('a', href=re.compile(r'/forezp/article/details'))
    for link in links:

        titles.add(link.get_text())


def parse_descrtion(html):
    if html is None:
        return None
    soup=BeautifulSoup(html, "html.parser")
    disciptions=soup.find_all('div',attrs={'class': 'article_description'})
    for link in disciptions:

        titles.add(link.get_text())


def jiebaSet():
    strs=''
    if titles.__len__()==0:
        return
    for item in titles:
        strs=strs+item;


    tags = jieba.analyse.extract_tags(strs, topK=100, withWeight=True)
    for item in tags:
        print(item[0] + '\t' + str(int(item[1] * 1000)))

def main():
   html= download(url)
   # parse_title(html)
   parse_descrtion(html)
   jiebaSet()


if __name__ == '__main__':
    main()
