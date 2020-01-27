import pandas as pd
import numpy as np
import requests
import bs4

from urllib.request import Request, urlopen
import time


# should install libraries - requests


address = pd.read_csv('data/Address.txt')

num_address = len(address.index)

# 인스타 주소에서 다른 정보를 가져오는 방법


def crawling_inform(address,csvtext):
    num_address = len(address)
    for i in range(0,num_address):
        csvtext.append([])
        req = Request('https://www.instagram.com'+address['Address'][i],headers={'User-Agent':'Mozilla/5.0'}) #Address열에 i번째부터 열기 시작
        # header에서 브라우저 버전을 탐지해 서버가 브라우저에 적합한 컨텐츠를 내려주도록 하는 것. 서버에서 브라우저를 탐지하기 위한 것이 User-Agent
        webpage = urlopen(req).read() #사이트의 정보를 가져와서 와서  읽어준다.

        soup = bs4.BeautifulSoup(webpage,"lxml",from_encoding='utf-8')



        #BeautifulSoup는 파이썬에서 사용하는 html parser lxml모듈이 빠르기 때문에 사용
        attribute = soup.find('meta',attrs={"property":"og:description"}) #meta 속성값이 같이 들어감 description : 요약내용을 정리해서 보여준다.

        site_content = attribute['content'] #위의 내용에서 내용만 뽑아서 저장해놓음

        find_id = site_content[site_content.find("@")+1:site_content.find(")")]
        find_id = find_id[:20]
        if find_id == "":
            find_id = 'Null'
        csvtext[i].append(find_id)

        for find_hashtag in soup.find_all('meta',attrs = {"property":"instapp:hashtags"}):
            find_hashtag = find_hashtag['content']
            csvtext[i].append(find_hashtag)

        find_like = site_content[:site_content.find('Likes')-1]
        csvtext[i].append(find_like)
    return csvtext



