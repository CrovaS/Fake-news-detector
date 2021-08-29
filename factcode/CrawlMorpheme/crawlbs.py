# crawlbs.py
# Written by Subin Kim (김수빈)

# crawlbs.py는 beautifulsoup4 라이브러리를 이용해 언론사별 크롤러를 구현해놓은 파일이다.
# 등등등...

# SPDX-FileCopyrightText: © 2021 Subin Kim <subinga18@naver.com>
# SPDX-License-Identifier: BSD-3-Clause

import requests
from bs4 import BeautifulSoup

from operator import eq


def selenium_or_not(press):
    # if press == 'naver':
    #     return 1
    # if press == '네이버':
    #     return 1
    # if press == 'Naver':
    #     return 1
    return -1


def crawl_news(query):
    news_url = '{}'
    title ='{}'
    article = '{}'
    journalist='{}'

    # 비정상적 요청이 아닌, user-agent 지정으로 크롬 브라우저에서의 요청인것으로 인식하게 함
    req = requests.get(news_url.format(query), headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(req.text, 'html.parser',from_encoding='euc-kr')

    media = query.split('.')[1]

    # 연합뉴스 210824 수정 완
    if eq(media,'yna'):
        press = 'yonhap'
        title = soup.select_one('#articleWrap > div.content03 > header > h1').get_text()
        article =''
        try: journalist = soup.select_one('#articleWrap > div.content01.scroll-article-zone01 > div > div > article > div.writer-zone > a > div > strong').get_text()
        except: journalist = 'a' 
        article_n = soup.find('article',{'class':'story-news article'})
        for p in article_n.find_all('p'):
            if p.string is None:
                p.string =''
            article = article+p.string
        
        article = article.replace('"','')
        article = article.replace("'","")
        article = article.replace('&apos;','')
        article = article.replace('@yna.co.kr','')
        article_list = article.split('. ')
        article = ''
        for sentence in article_list:
            article = article + sentence + '.\n'

    # 네이버 뉴스
    elif eq(media,'naver'):
        press = 'naver'
        title = soup.select_one('h3#articleTitle').get_text()
        article = soup.select_one('#articleBodyContents').get_text()
        journalist = soup.select_one('#articleBody > div.byline > p').get_text()

    # 다음 뉴스
    elif eq(media,'v'):
        press = 'daum'
        title = soup.select_one('#cSub > div > h3').get_text()
        article = soup.select_one('#mArticle > div > div.news_view').get_text()
        journalist = soup.select_one('#harmonyContainer > section > address').get_text()

    # 동아일보 
    # 본문 부분이 너무 안나뉘어 있어서 일단 article 전체를 긁어오긴 했지만 수정 필요 >> 사진 부터 전체 다 긁혀서 문제 있음 
    elif eq(media,'donga'):
        press = 'donga'
        title = soup.select_one('head > title').get_text()
        article = soup.select_one('#content > div > div.article_txt').get_text()
        journalist = soup.select_one('#container > div.article_title > div.title_foot > span.report').get_text()

   # 중앙일보 0823 수정 완 
    elif eq(media,'joins'):
        press = 'joongang'
        title = soup.select_one('#container > section > article > header > h1').get_text().strip()
        article=''
        article_n = soup.find('div',{'class':'article_body fs3'})
        for p in article_n.find_all('p'):
            if p.string is None:
                p.string =''
            article = article + p.string
        journalist = soup.select_one('#article_body > div.ab_byline').get_text()


    # 경향 신문 0823 수정 완
    elif eq(media,'khan'):
        press = 'kyunghyang'
        title = soup.select_one('#article_title').get_text()
        article=''
        article_n = soup.select('#articleBody > p')
        for p in article_n :
            article = article + p.text
        journalist = soup.select_one('#container > div.art_header.borderless > div.function_wrap > div.art_info > span > a').get_text()
    
    # 국민일보 
    # 한글 깨짐 수정 요망
    elif eq(media,'kmib'):
        press = 'kookmin'
        title = soup.select_one('#sub > div.sub_header > div > div.nwsti').get_text()
        article = soup.select_one('#articleBody').get_text()
        #journalist = soup.select_one('#container > div.article_title > div.title_foot > span.report').get_text()

    #뉴스 1 
    #한글 깨짐 수정 요망 
    elif eq(media,'news1'):
        press = 'news1'
        title = soup.select_one('#article_body_content > div.title > h2').get_text()
        article = soup.select_one('#articles_detail').get_text()
        journalist = soup.select_one('#article_body_content > div.title > div.info').get_text()

    #뉴시스
    elif eq(media,'newsis'):
        press = 'newsis'
        title = soup.select_one('').get_text()
        article = soup.select_one('').get_text()
        journalist = soup.select_one('').get_text()

    #문화 일보 
    elif eq(media,'munhwa'):
        press = 'munhwa'
        title = soup.select_one('').get_text()
        article = soup.select_one('').get_text()
        journalist = soup.select_one('').get_text()

    #서울 신문 
    elif eq(media,'seoul'):
        press = 'seoul'
        title = soup.select_one('').get_text()
        article = soup.select_one('').get_text()
        journalist = soup.select_one('').get_text()

    #세계 일보 
    elif eq(media,'segye'):
        press = 'segye'
        title = soup.select_one('').get_text()
        article = soup.select_one('').get_text()
        journalist = soup.select_one('').get_text()

    #조선 일보 
    elif eq(media,'chosun'):
        press = 'chosun'
        title = soup.select_one('').get_text()
        article = soup.select_one('').get_text()
        journalist = soup.select_one('').get_text()

    #한겨례
    elif eq(media,'hani'):
        press = 'hankyoreh'
        title = soup.select_one('').get_text()
        article = soup.select_one('').get_text()
        journalist = soup.select_one('').get_text()

    #한국 일보 
    elif eq(media,'hankookilbo'):
        press = 'hankook'
        title = soup.select_one('').get_text()
        article = soup.select_one('t').get_text()
        journalist = soup.select_one('').get_text()

    else :
        print("This press is not ready yet.")

    return press, journalist, title, article


if __name__ == '__main__':
    query = input ('기사 링크를 입력하세요 : ')

    press, reporter, title, article = crawl_news(query)
    print(title)
    print(article)
    print(reporter)
    print(press)