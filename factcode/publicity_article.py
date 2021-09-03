# publicity_article.py
# Written by Byeongho Hwang (황병호)

# model_factcheck.py가 전반적인 기능을 크게 구현해놓은 연결이라고 한다면,
# publicity_article.py는 그 메이저 모듈 중 하나인 홍보성 기사 감지 기능의
# 각 기능의 세부 기능과 흐름을 구현해놓은 것이다.

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause

# (2) Publicity Article Checker
# Functions Required::
# positivity_checker()
# propernoun_search()
# sudden_leap()
# conjunction_association()
# evaluation_moduleB()

# sdk에서 url 배포를 위해 실행시킬 경우 아래 모듈을 사용, 위 모듈은 주석 처리
try:
    from factcode.CrawlMorpheme import crawlmorpheme
    from factcode.PositivityCheck import positivity_test
    from factcode.StringProcess import propernoun
    from factcode.Optimization import sudden
    from factcode.Optimization import conjunction
    from factcode import settingbox
# 로컬 컴퓨터로 실행시킬 경우 위 모듈을 사용, 아래 모듈은 주석 처리
except:
    from CrawlMorpheme import crawlmorpheme
    from PositivityCheck import positivity_test
    from StringProcess import propernoun
    from Optimization import sudden
    from Optimization import conjunction
    import settingbox

# from factcode.CrawlMorpheme import crawlmorpheme
# from factcode.PositivityCheck import positivity_test
# from factcode.StringProcess import propernoun
# from factcode.Optimization import sudden
# from factcode.Optimization import conjunction
# from factcode import settingbox

cm = crawlmorpheme
pc = positivity_test
pn = propernoun
sd = sudden
cj = conjunction

# 긍정/부정 정도 측정은 인공지능 모델을 통해 이루어진다.
# 인공지능 모델이 문장을 단위로 긍정/부정을 판별하므로
# 유형에 맞추어 텍스트를 문장 단위로 쪼개주고, 문단 단위로 긍정 정도를 계산해야한다.
def positivity_checker(text, mode = 'context'):

    if mode == 'title':
        positivity = pc.use_positivity_model(text)
        return positivity
    
    if mode == 'context':
        paragraph_arr = text.split('\n')
        positivity = []
        for paragraph in paragraph_arr:
            sentence_arr = paragraph.split('.')
            sentence_positivity_sum = 0
            sentence_count = 0
            for sentence in sentence_arr:
                if len(sentence) < 3: pass
                else:
                    try:
                        positivity_sen = pc.use_positivity_model(sentence)
                        print(positivity_sen)
                        sentence_count = sentence_count + 1
                        sentence_positivity_sum = sentence_positivity_sum + positivity_sen
                    except: pass
            if sentence_count == 0: pass
            else:
                temp_positivity = sentence_positivity_sum/sentence_count
                positivity.append(temp_positivity)
        return positivity

# 고유명사 판별은 키스티의 기관 검색을 이용한다.
# 페이지의 보안에 따라 url을 통해 검색을 진행할 수 없고,
# 오로지 실제 태그와 브라우저 조종을 이용해서만 검색이 가능하기 때문에
# selenium 라이브러리를 이용해 실제 드라이버로 브라우저를 열어 검색을 진행한다.
def propernoun_search(text1, text2):
    propernoun_array1 = []
    propernoun_array2 = []
    driver_path = settingbox.get_directory('chromedriver')
    noun_arr1 = cm.get_noun_array(text1)
    noun_arr2 = []
    text2_arr = text2.split('\n')
    for paragraph in text2_arr:
        if len(paragraph) > 2:
            arraycomponent = cm.get_noun_array(paragraph)
            noun_arr2.append(arraycomponent)
    propernoun_array1, propernoun_array2 = pn.search_propernoun(noun_arr1, noun_arr2, driver_path = driver_path)
    return propernoun_array1, propernoun_array2

# 홍보하고자 하는 제시어가 나왔을 때 문장이 어느 정도로 긍정적이게 제시되느냐를 계산한다.
def sudden_leap(pos_title, pos_summary, arr_title, arr_content):
    # data type: pos_title - float, pos_summary - float array, arr_title - string array, arr_content - string array
    sudden_leap_degree = sd.leap(pos_title, pos_summary, arr_title, arr_content)
    return sudden_leap_degree

# 접속사를 이용해 state를 구분, 물건을 홍보하고자 하는 목적이 어느 정도나 있는지 확인한다.
def conjunction_association(text):
    conjunction_check = cj.check(text)
    return conjunction_check

# 홍보성 기사 점수 계산
def evaluation_moduleB(num1, num2, param_arrayB):
    reliability_2 = num1 * param_arrayB[0] + num2 * param_arrayB[1] + param_arrayB[2]
    return reliability_2