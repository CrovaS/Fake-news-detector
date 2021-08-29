# crawlmorpheme.py
# Written by Subin Kim (김수빈)
# Editted by Byeongho Hwang (황병호)

# crawlmorpheme.py는 간이 크롤러와 형태소 분석기를 가공한 다양한 함수들을 관리하는 파일이다.
# 등등등...

# SPDX-FileCopyrightText: © 2021 Subin Kim <subinga18@naver.com>
# SPDX-License-Identifier: BSD-3-Clause

import requests
from bs4 import BeautifulSoup

# Import JPype for Konlpy
try:
    import jpype
    import jpype1
except:
    import jpype

# Import NLP
from konlpy.tag import Okt
from collections import Counter
import gensim

from pandas import DataFrame 
import re
import os
import pandas as pd
import numpy as np

# !pip install gensim==3.8.1

def crawl_navernews(query):
    news_url = '{}'

    # 비정상적 요청이 아닌, user-agent 지정으로 크롬 브라우저에서의 요청인것으로 인식하게 함
    req = requests.get(news_url.format(query), headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(req.text, 'html.parser')

    # 네이버 뉴스 부분에서 파싱
    title = soup.select_one('h3#articleTitle').get_text()
    article = soup.select_one('#articleBodyContents').get_text()
    journalist = soup.select_one('#articleBody > div.byline > p').get_text()
    return title, article, journalist

def get_morpheme(text):
    okt = Okt()
    morpheme_arr = okt.pos(text)
    return morpheme_arr

def get_morpheme_dataframe(text):
    okt = Okt()
    morpheme_dataframe = pd.DataFrame (okt.pos(text),columns=['word','pos'])
    return morpheme_dataframe

def get_morpheme_dataframe_nouns(text):
    okt = Okt()
    morpheme_dataframe = pd.DataFrame (okt.pos(text),columns=['word','pos'])
    morpheme_dataframe_nouns = morpheme_dataframe[morpheme_dataframe['pos']=='Noun']
    return morpheme_dataframe_nouns

def get_noun_array(text):
    okt = Okt()
    noun_text = okt.nouns(text)
    return noun_text

def often_top_n(text, n=10):
    # okt 객체 생성
    okt = Okt()
    noun_text = okt.nouns(text)

    # 한글자인 명사 빼는 부분 >> 등, 고, 줌, 외 같은게 명사로 들어가있음
    for i, v in enumerate(noun_text):
        if len(v) < 2:
            noun_text.pop(i)

    # 본문 명사 빈도 카운트 후 top 100 저장, (단어, 빈도수) 형태로 저장됨
    count = Counter(noun_text)
    top_n = count.most_common(n)

    # top 10 중 단어만 추출하여 top_10_list로 저장
    top_n_list = []
    for v in top_n:
        top_n_list.append(v[0])

    return top_n_list

def morpheme_model_AA(noun_title ,top_10_list):
    # 형태소 분석 모델
    # 노트북 속 ko.bin 파일 위치 넣기
    model = gensim.models.Word2Vec.load('C:/Ekenda Bia/Fact Checker/factChecker/factcode/CrawlMorpheme/content/ko.bin')

    # 본문 속 빈도수 top 10 단어끼리의 연관성
    # top 10 끼리의 연관성 계산 > 이미 계산한 연관성 반복 없게 하려고 이중 포문 저렇게 작성
    sort_w1 = []
    sort_w2 = []
    sort_result = []  # 문자열 형태로 저장된 결과물
    f_sort_result = []  # float 형식으로 재저장할 것

    for k in range(9):
        for j in range(k+1, 10):
            try:
                # top10 끼리의 similarity 계산
                result = model.wv.similarity(top_10_list[k], top_10_list[j])
                # 새로운 배열에 각각 저장
                sort_w1.append(top_10_list[k])
                sort_w2.append(top_10_list[j])
                sort_result.append(result)
                f_sort_result = list(map(float, sort_result))
            except:
                pass


    # buble sort를 이용한 오름차순 sorting의 결과물
    # 10개끼리 비교하는 거라 range(45)임
    # print("article & article -- after sorted ------")
    for i in range(45):
        for j in range(45-i-1):
            try:
                if f_sort_result[j] > f_sort_result[j+1]:
                    # result 자리 변경
                    temp = f_sort_result[j]
                    f_sort_result[j] = f_sort_result[j+1]
                    f_sort_result[j+1] = temp
                    # 단어1 자리 변경
                    temp_w1 = sort_w1[j]
                    sort_w1[j] = sort_w1[j+1]
                    sort_w1[j+1] = temp_w1
                    # 단어2 자리 변경
                    temp_w2 = sort_w2[j]
                    sort_w2[j] = sort_w2[j+1]
                    sort_w2[j+1] = temp_w2
            except:
                pass

    res_1 = 0
    res_2 = 0
    for k in range(len(f_sort_result)):
        try:
            if f_sort_result[k]<1:
                res_1 = res_1 + 1
                res_2 = res_2 + f_sort_result[k]
        except:
            pass
    res_A = res_2/res_1

    # 제목 속 모든 명사 & 본문 속 빈도 top 10 단어 사이의 연관성
    # 상단의 본문 & 본문과 기능 면에서는 유사함
    a_sort_w1 = []  # 제목
    a_sort_w2 = []  # 본문
    a_sort_result = []
    fa_sort_result = []

    # 제목 전체 순회 ( 제목의 명사 갯수는 기사마다 다를 것이기 때문에 len 사용 )
    for k in range(len(noun_title)):
        # top 10은 10개니까 10개 순회
        for j in range(10):
            try:
                result = model.wv.similarity(noun_title[k], top_10_list[j])
                a_sort_w1.append(noun_title[k])
                a_sort_w2.append(top_10_list[j])
                a_sort_result.append(result)
                fa_sort_result = list(map(float, a_sort_result))
            except:
                pass

    print()

    # bubble sort후 오름차순 결과물
    # 결과물의 길이와 범위가 일치할 것이기 때문에 len(fa_sort_result)
    # print("title & article -- after sorted ------")
    for i in range(len(fa_sort_result)):
        for j in range(len(fa_sort_result)-i-1):
            try:
                if fa_sort_result[j] > fa_sort_result[j+1]:
                    # result 자리 변경
                    temp = fa_sort_result[j]
                    fa_sort_result[j] = fa_sort_result[j+1]
                    fa_sort_result[j+1] = temp
                    # title w1 자리 변경
                    temp_w1 = a_sort_w1[j]
                    a_sort_w1[j] = a_sort_w1[j+1]
                    a_sort_w1[j+1] = temp_w1
                    # 본문 w2 자리 변경
                    temp_w2 = a_sort_w2[j]
                    a_sort_w2[j] = a_sort_w2[j+1]
                    a_sort_w2[j+1] = temp_w2
            except:
                pass

    res_3 = 0
    res_4 = 0

    for k in range(len(fa_sort_result)):
        try:
            if fa_sort_result[k]<1:
                res_3 = res_1 + 1
                res_4 = res_2 + fa_sort_result[k]
        except:
            pass

    res_B = (res_4/res_3)
    print (str(res_A)+', '+str(res_B))

    result = 100/(2.718281**((-1)*(res_B/res_A))+1)
    return result

def morpheme_model_BB(top_10_list_A ,top_10_list_B):
    # 형태소 분석 모델
    # 노트북 속 ko.bin 파일 위치 넣기
    model = gensim.models.Word2Vec.load('C:/Ekenda Bia/Fact Checker/factChecker/factcode/CrawlMorpheme/content/ko.bin')

    # 본문 속 빈도수 top 10 단어끼리의 연관성
    # top 10 끼리의 연관성 계산 > 이미 계산한 연관성 반복 없게 하려고 이중 포문 저렇게 작성
    a_sort_w1 = []
    a_sort_w2 = []
    a_sort_result = []  # 문자열 형태로 저장된 결과물
    fa_sort_result = []  # float 형식으로 재저장할 것

    for k in range(9):
        for j in range(k+1, 10):
            try:
                # top10 끼리의 similarity 계산
                result = model.wv.similarity(top_10_list_A[k], top_10_list_A[j])
                # 새로운 배열에 각각 저장
                a_sort_w1.append(top_10_list_A[k])
                a_sort_w2.append(top_10_list_A[j])
                a_sort_result.append(result)
                fa_sort_result = list(map(float, a_sort_result))
            except:
                pass


    # buble sort를 이용한 오름차순 sorting의 결과물
    # 10개끼리 비교하는 거라 range(45)임
    # print("article & article -- after sorted ------")
    for i in range(45):
        for j in range(45-i-1):
            try:
                if fa_sort_result[j] > fa_sort_result[j+1]:
                    # result 자리 변경
                    temp = fa_sort_result[j]
                    fa_sort_result[j] = fa_sort_result[j+1]
                    fa_sort_result[j+1] = temp
                    # 단어1 자리 변경
                    temp_w1 = a_sort_w1[j]
                    a_sort_w1[j] = a_sort_w1[j+1]
                    a_sort_w1[j+1] = temp_w1
                    # 단어2 자리 변경
                    temp_w2 = a_sort_w2[j]
                    a_sort_w2[j] = a_sort_w2[j+1]
                    a_sort_w2[j+1] = temp_w2
            except:
                pass

    res_1 = 0
    res_2 = 0
    for k in range(len(fa_sort_result)):
        try:
            if fa_sort_result[k]<1:
                res_1 = res_1 + 1
                res_2 = res_2 + fa_sort_result[k]
        except:
            pass
    if res_1 == 0: res_A = 1
    else: res_A = res_2/res_1

    # 본문 속 빈도수 top 10 단어끼리의 연관성
    # top 10 끼리의 연관성 계산 > 이미 계산한 연관성 반복 없게 하려고 이중 포문 저렇게 작성
    b_sort_w1 = []
    b_sort_w2 = []
    b_sort_result = []  # 문자열 형태로 저장된 결과물
    fb_sort_result = []  # float 형식으로 재저장할 것

    for k in range(9):
        for j in range(k+1, 10):
            try:
                # top10 끼리의 similarity 계산
                result = model.wv.similarity(top_10_list_B[k], top_10_list_B[j])
                # 새로운 배열에 각각 저장
                b_sort_w1.append(top_10_list_B[k])
                b_sort_w2.append(top_10_list_B[j])
                b_sort_result.append(result)
                fb_sort_result = list(map(float, b_sort_result))
            except:
                pass


    # buble sort를 이용한 오름차순 sorting의 결과물
    # 10개끼리 비교하는 거라 range(45)임
    # print("article & article -- after sorted ------")
    for i in range(45):
        for j in range(45-i-1):
            try:
                if fb_sort_result[j] > fb_sort_result[j+1]:
                    # result 자리 변경
                    temp = fb_sort_result[j]
                    fb_sort_result[j] = fb_sort_result[j+1]
                    fb_sort_result[j+1] = temp
                    # 단어1 자리 변경
                    temp_w1 = b_sort_w1[j]
                    b_sort_w1[j] = b_sort_w1[j+1]
                    b_sort_w1[j+1] = temp_w1
                    # 단어2 자리 변경
                    temp_w2 = b_sort_w2[j]
                    b_sort_w2[j] = b_sort_w2[j+1]
                    b_sort_w2[j+1] = temp_w2
            except:
                pass

    res_3 = 0
    res_4 = 0
    for k in range(len(fb_sort_result)):
        try:
            if fb_sort_result[k]<1:
                res_3 = res_3 + 1
                res_4 = res_4 + fb_sort_result[k]
        except:
            pass
    if res_3 == 0: res_B = 1
    else: res_B = res_4/res_3

    # 본문 속 빈도수 top 10 단어끼리의 연관성
    # top 10 끼리의 연관성 계산 > 이미 계산한 연관성 반복 없게 하려고 이중 포문 저렇게 작성
    ab_sort_w1 = []
    ab_sort_w2 = []
    ab_sort_result = []  # 문자열 형태로 저장된 결과물
    fab_sort_result = []  # float 형식으로 재저장할 것

    for k in range(9):
        for j in range(k+1, 10):
            try:
                # top10 끼리의 similarity 계산
                result = model.wv.similarity(top_10_list_A[k], top_10_list_B[j])
                # 새로운 배열에 각각 저장
                ab_sort_w1.append(top_10_list_A[k])
                ab_sort_w2.append(top_10_list_B[j])
                ab_sort_result.append(result)
                fab_sort_result = list(map(float, ab_sort_result))
            except:
                pass


    # buble sort를 이용한 오름차순 sorting의 결과물
    # 10개끼리 비교하는 거라 range(45)임
    # print("article & article -- after sorted ------")
    for i in range(45):
        for j in range(45-i-1):
            try:
                if fab_sort_result[j] > fab_sort_result[j+1]:
                    # result 자리 변경
                    temp = fab_sort_result[j]
                    fab_sort_result[j] = fab_sort_result[j+1]
                    fab_sort_result[j+1] = temp
                    # 단어1 자리 변경
                    temp_w1 = ab_sort_w1[j]
                    ab_sort_w1[j] = ab_sort_w1[j+1]
                    ab_sort_w1[j+1] = temp_w1
                    # 단어2 자리 변경
                    temp_w2 = ab_sort_w2[j]
                    ab_sort_w2[j] = ab_sort_w2[j+1]
                    ab_sort_w2[j+1] = temp_w2
            except:
                pass

    res_5 = 0
    res_6 = 0
    for k in range(len(fab_sort_result)):
        try:
            if fab_sort_result[k]<1:
                res_5 = res_5 + 1
                res_6 = res_6 + fab_sort_result[k]
        except:
            pass
    if res_5 == 0: res_AB = 1
    else: res_AB = res_6/res_5

    # res_A: WordtoVec at A
    # res_B: WordtoVec at B
    # res_AB: WordtoVec between AB
    result = 50*(abs(res_AB-res_A)+abs(res_AB-res_B)+abs(res_A-res_B))
    
    return result

if __name__ == '__main__':
    # query = input ('기사 링크를 입력하세요 : ')
    query = 'https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=100&oid=001&aid=0012579586'
    title, article, journalist = crawl_navernews(query)
    noun_title = often_top_n(title)
    top_10_list_B = often_top_n(article)
    morpheme_model_AA(noun_title ,top_10_list_B)
