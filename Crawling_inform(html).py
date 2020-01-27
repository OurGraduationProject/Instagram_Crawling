from urllib import parse
from selenium import webdriver
import time
import bs4
import selenium
import pandas as pd
import Crawling_inform
import numpy as np

driver = selenium.webdriver.Chrome('Chrome driver/chromedriver.exe')
address = pd.read_csv('data/구정동맛집txt')




inform_csvtext = []
csvtext = []


def crawling_insta(num_address):

    for i in range(0,num_address):
        inform_csvtext.append([])

        page = 'https://www.instagram.com'+address['Address'][i]
        driver.get(page)
        time.sleep(1)
        raw_source = driver.page_source
        refined_source = bs4.BeautifulSoup(raw_source, 'lxml')
        time_data = refined_source.find('time',attrs={"class":"_1o9PC Nzb55"})
        csvtext[i].append(time_data.string)


def changed_csv(csv):
    changed_csv = []
    for i in range(0,len(csv)):
        line = []
        for j in range(0,1):
            line.append(csv[i][0])
            line.append("/".join(csv[i][1:-2]))
            line.append(csv[i][-2])
            line.append(csv[i][-1])
        changed_csv.append(line)
    return changed_csv


if __name__ == "__main__":
    num_address = len(address.index)
    test = Crawling_inform.crawling_inform(address,csvtext)
    crawling_insta(num_address)
    changed_csv = changed_csv(csvtext)
    print(changed_csv)
    pd_csv = pd.DataFrame(changed_csv, columns=['id', 'hashtags', 'likes', 'date'])

    # \xa0, \xa9 를 없애줌

    # encoding: cp949 로 전환--> 엑셀에서 깨지지 않게
    pd_csv.to_csv("test_2.csv",sep=',',encoding="utf-8")

