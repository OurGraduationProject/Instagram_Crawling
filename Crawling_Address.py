import selenium
from urllib import parse
from selenium import webdriver
import time
import bs4
import selenium
import pandas as pd

# should install libraries - Beautifulsoup4, selenium, lxml

search = input('검색어 입력 : ')
search = parse.quote(search)
url = 'https://www.instagram.com/explore/tags/' + str(search)+ '/'

driver = selenium.webdriver.Chrome('Chrome driver/chromedriver.exe')
driver.get(url)
time.sleep(5)

SCROLL_PAUSE_TIME = 1.0
reallink = []

while True:
    pageString = driver.page_source # page_source에서 웹 Page의 코딩을 가져올 수 있음.
    bsObj = bs4.BeautifulSoup(pageString, 'lxml')  # https://brownbears.tistory.com/414 정보

    """
    a = bsObj.find_all(name='div',attrs={"class":"Nnq7C weEfm"}) div에서 Nnq7c 클래스 모두 찾아서 a에 저장
    b = a[0].select('a')[0]  (1,3) 행,열이 쭉 아래로 내려가는 형태로 되어 있어 a[x].select('a')[y]에서 x는 행번호, y는 열번호 라 생각하면 편하다.
    c = b.attrs['href']
    print(b)
    print(c)
    """
    try:
        for link1 in bsObj.find_all(name='div',attrs={"class":"Nnq7C weEfm"}):
            title = link1.select('a')[0]
            real = title.attrs['href']
            reallink.append(real) # 이미지의 사이트 href를 reallink리스트에 추가
            title = link1.select('a')[1]
            real = title.attrs['href']
            reallink.append(real)
            title = link1.select('a')[2]
            real = title.attrs['href']
            reallink.append(real)
    except:
        print("인덱스가 없습니다.")


# 인스타가 업데이트 class도 동적으로 업데이트되어 크롤링 했던 사이트는 빠지고 새로운 스크롤부터 시작함
    last_height = driver.execute_script("return document.body.scrollHeight") #execute_script를 이용해 자바스크립트 사용
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") #https://m.blog.naver.com/PostView.nhn?blogId=seilius&logNo=130166947739&proxyReferer=https%3A%2F%2Fwww.google.com%2F
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height: #  잘못 멈출 수 있기 때문에 서버에서 받아오는 시간을 1초더 기다려줌
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height: # 비교 값이 같으면 모두 내려갔다 생각하고 종료
            break
        else:
            last_height = new_height
            continue

print(reallink[5])
print("모든 사이트를 입력 하였습니다.")
data = pd.DataFrame(reallink)
data.index.name = "sequence"
data.columns=['Address']
print(data)
name = input("저장할 파일의 이름을 정해주십시오 :")
data.to_csv("data/"+name + '.txt',encoding='utf-8', index = False)

# https://rfriend.tistory.com/252 data.to_csv 환경설정