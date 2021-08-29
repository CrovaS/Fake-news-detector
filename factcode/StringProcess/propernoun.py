# coding:utf-8
# 1번 줄의 주석은 주석이 아닌 코드의 부분으로, 지우면 코드가 작동하지 않으므로 주의.

# propernoun.py
# Written by Yunji Lee (이윤지)
# Editted by Byeongho Hwang (황병호)

# propernoun.py는 키스티의 기관검색창을 열어 기업/기관 여부를 확인하는 파일이다.
# 등등등...

# SPDX-FileCopyrightText: © 2021 Yunji Lee <qwerty5098@kyonggi.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def search_propernoun(noun_arr1, noun_arr2, driver_path):
    SCROLL_PAUSE_TIME = 0.05
    print(str(noun_arr1)+"-----------"+str(noun_arr2))
    searcharray_1 = []
    searcharray_2 = []
    for noun1 in noun_arr1:
        if len(noun1) > 2: searcharray_1.append(noun1)
    for paragraph_noun in noun_arr2:
        paragraph_noun_arr = []
        for noun2 in paragraph_noun:
            if len(noun2) > 2: paragraph_noun_arr.append(noun2)
        searcharray_2.append(paragraph_noun_arr)


    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # driver = webdriver.Chrome(executable_path='C:/Ekenda Bia/Fact Checker/factChecker/selenium/chromedriver.exe', options=options)
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    # driver = webdriver.Chrome()
    driver.get("https://nrms.kisti.re.kr/cm/common/inst_info.do")
    
    inputcrp = driver.find_element_by_id("KOR_INST_NM")
    elem = driver.find_element_by_id("search")

    propernoun_arr1 = []
    for nounA in searcharray_1:
        inputcrp.clear()
        inputcrp.send_keys(nounA)
        elem.click()
        try:
            time.sleep(SCROLL_PAUSE_TIME)
            checkera = driver.find_elements_by_class_name("ui-paging-info")
            checker = checkera.text
            # print("------title checker")
            # print(nounA+" : "+checker)
            # print(checker)
            if checker != '데이터가 없습니다.': propernoun_arr1.append(nounA)
        except:
            # print("pass")
            pass

    propernoun_arr2 = []
    for paragraph_nouns in searcharray_2:
        propernoun_semiarr2 = []
        for nounB in paragraph_nouns:
            inputcrp.clear()
            inputcrp.send_keys(nounB)
            elem.click()
            try:
                time.sleep(SCROLL_PAUSE_TIME)
                checkera = driver.find_element_by_class_name("ui-paging-info")
                checker = checkera.text
                # print("------content checker")
                # print(nounB+" : "+checker)
                if checker != '데이터가 없습니다.': propernoun_semiarr2.append(nounB)
            except:
                # print("pass")
                pass
        propernoun_arr2.append(propernoun_semiarr2)

    driver.close()
    # print("--------------------")
    # print(propernoun_arr1)
    # print(propernoun_arr2)
    # print("--------------------")

    return propernoun_arr1, propernoun_arr2

if __name__ == '__main__':
    noun_title = ['한미', '연합', '훈련', '연기', '예정', '시행', '규모', '축소']
    noun_content = [['오류', '우회', '위', '함수', '추가'], [], ['국방부', '시기', '규모', '미확정', '협의', '사전', '준비', '착수', '한미', '연합', '훈련', '축소', '실시', '전망', '정연주', '제작', '일러스트', '서울', '연합뉴스', '김', '기자', '여권', '일각', '한미', '연합', '훈련', '연기론', '확산', '가운데', '한국', '미국', '군', '당국', '신종', '코로나바이러스', '감염증', '코로나', '상황', '등', '고려', '규모', '축소', '실시', '전망', '국방부', '후반기', '훈련', '시기', '규모', '등', '확정', '양국', '협의', '중이', '입장', '거듭', '부승찬', '국방부', '대변인', '정례', '브리핑', '관련', '질의', '하반기', '연합', '훈련', '시기', '규모', '방식', '확정', '며', '한미', '이', '관련', '각종', '여건', '종합', '고려', '협의', '고', '답', '한미', '군', '당국', '사전', '연습', '성격', '위기', '관리', '참모', '훈련', '후반기', '연합', '지휘', '훈련', '각각', '진행', '일정', '훈련', '준비', '중인', '것', '앞서', '문재인', '대통령', '전날', '이번', '달', '예정', '한미', '연합', '훈련', '관련', '여러', '가지', '고려', '미국', '측', '협의', '고', '말', '문', '대통령', '군', '주요', '지휘', '관', '국방', '현안', '보고', '자리', '서욱', '국방부', '장관', '한미', '연합', '훈련', '관련', '현재', '코로나', '상황', '등', '현실', '여건', '감안', '방역', '당국', '및', '미국', '측', '협의', '중', '보고', '언급', '청와대', '핵심', '관계자', '전', '이', '범여', '의원', '여', '명', '연합', '훈련', '연기', '등', '연기론', '확산', '이', '군', '관계자', '한미', '내주', '연습', '위', '토론', '전체', '훈련', '시나리오', '점검', '등', '훈련', '준비', '시작', '고', '전', '다른', '관계자', '현재', '한미연합사령부', '합참', '등', '군', '내부', '분위기', '훈련', '쪽', '말', '군', '일각', '한미', '군', '당국', '시작', '것', '예상', '훈련', '직전', '시기', '규모', '등', '대한', '발표', '것', '예상', '계획', '일정', '훈련', '시작', '코로나', '확산', '세', '등', '고려', '규모', '축소', '훈련', '시설', '벙커', '여건', '밀', '밀접', '밀집', '밀폐', '환경', '노출', '수', '참여', '인원', '대폭', '때문', '군', '관계자', '반기', '연합', '지휘', '훈련', '수준', '예상', '고', '말']]
    check = search_propernoun(noun_title, noun_content)
    print(check)