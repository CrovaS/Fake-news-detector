# coding:utf-8
# 1번 줄의 주석은 주석이 아닌 코드의 부분으로, 지우면 코드가 작동하지 않으므로 주의.

# model_factcheck.py
# Written by Byeongho Hwang (황병호)

# model_factcheck.py는 구체적인 가짜뉴스 판별기를 구현해놓은 파일로,
# 각 메이저 모듈의 전체 과정이 표현되어 있다.

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause

# 모듈 태그: 세 가지 기능을 하는 모듈과 테스트용 파일을 가져온다.
# 메이저 모듈 이외에 필요한 크롤링 도구와 문자열 재구성 등을 할 수 있는 파일도 가져온다.
# [START Module tagging]

# sdk에서 url 배포를 위해 실행시킬 경우 위 모듈을 사용
try:
    from factcode import provocative_title
    from factcode import publicity_article
    from factcode import republishing_same
    from factcode.StringProcess import summaries
    from factcode.CrawlMorpheme import crawlbs
    from factcode.CrawlMorpheme import crawlsl
# 로컬 컴퓨터로 실행시킬 경우 아래 모듈을 사용
except:
    import provocative_title
    import publicity_article
    import republishing_same
    from StringProcess import summaries
    from CrawlMorpheme import crawlbs
    from CrawlMorpheme import crawlsl

# from factcode import provocative_title
# from factcode import publicity_article
# from factcode import republishing_same
# from factcode import stringbox
# from factcode.StringProcess import summaries
# from factcode.CrawlMorpheme import crawlbs
# from factcode.CrawlMorpheme import crawlsl

modA = provocative_title
modB = publicity_article
modC = republishing_same
strp = summaries
crbs = crawlbs
crsl = crawlsl
# [END Module tagging]

# 크롤링: 페이지의 보안 설정에 따라 어떤 라이브러리를 사용할 지 구분한 뒤,
# 사용할 라이브러리에 맞추어 링크를 가공해 필요한 정보를 얻는다.
# [START Crawling]
def get_titleAndContents(link):
    checker = crbs.selenium_or_not(link)
    if checker == 1:
        press, reporter, articletitle, articlecontents = crsl.crawl_allsl(link)
    elif checker == -1:
        press, reporter, articletitle, articlecontents = crbs.crawl_news(link)
    else:
        press = None
        reporter = None
        articletitle = None
        articlecontents = None
    return press, reporter, articletitle, articlecontents
# [END Crawling]

# 스트링 가공: 본문을 그대로 가져다 쓰면 기사가 너무 길어지기 때문에,
# 각 필요에 맞추어 시간이 오래 걸리는 모듈에는 요약본을 사용해야한다.
# [START Summarizing]
def get_summary(articletitle, articlecontents, classification):

    if classification == 1:
        summary = strp.sum1(articletitle, articlecontents)
    elif classification == 2:
        summary = strp.sum2(articletitle, articlecontents)
    elif classification == 3:
        summary = strp.sum3(articletitle, articlecontents)
    elif classification == 4:
        summary = strp.sum4(articletitle, articlecontents)
    elif classification == 5:
        summary = strp.sum5(articletitle, articlecontents)
    else:
        summary = ''
    
    return summary
# [END Summarizing]


# [START Major Module]
# Running modules
# 팩트체커에는 세 가지 메이저 모듈이 존재한다.
# Three modules are in the factchecker:
# 1. Provoactive Title Checker (자극적인 제목 감지)
# 2. Publicity Article Checker (홍보성 기사 감지)
# 3. Republishing Same Article Checker (같은 기사 재업로드)

# (1) Provocative Title Checker
# Functions Required::
# morpheme_separation() - 형태소를 분리하는 역할
# causal_comparison() - 조사를 이용해 단어간 인과관계 파악
# WordtoVec_exclusiveA() - 단어간의 연관성 계산
# evaluation_moduleA() - 자극적 제목 정도 계산

def provocative_title_checker(articletitle, summary1, summary2):
    # Causal Relationship Comparison
    # 인과관계 비교
    morpheme1 = modA.morpheme_separation(articletitle)
    morpheme2 = modA.morpheme_separation(summary1)
    relation_similarity = modA.causal_comparison(morpheme1, morpheme2)
    # print(relation_similarity)

    # Word2Vec AI Model
    # 워드투벡터 인공지능 모델
    WordtoVec_result = modA.WordtoVec_exclusiveA(articletitle, summary2)
    # print(WordtoVec_result)

    # Final Score Evaluation
    reliability_1 = modA.evaluation_moduleA(relation_similarity, WordtoVec_result, param_arrayA=[0.5,0.5,0])
    return reliability_1

# (2) Publicity Article Checker
# Functions Required::
# positivity_checker() - 긍정/부정 정도 측정
# propernoun_search() - 고유명사 여부 판별
# sudden_leap() - 제품이 소개됨과 동시에 분위기의 전환 정도 계산
# conjunction_association() - 접속사 연결관계 파악
# evaluation_moduleB() - 홍보성 기사 정도 계산

def publicity_article_checker(articletitle, summary3, summary4):
    # Propernoun-Atmosphere Relation Check
    # 고유명사 - 분위기 연관도 체크
    positivity_title = modB.positivity_checker(articletitle, mode = 'title')
    positivity_summary = modB.positivity_checker(summary3, mode = 'context')
    propernoun_titlesearch, propernoun_contentsearch = modB.propernoun_search(articletitle, summary3)
    sudden_leap_degree = modB.sudden_leap(positivity_title, positivity_summary, propernoun_titlesearch, propernoun_contentsearch)
    # print(sudden_leap_degree)

    # Conjuction Association
    # 접속사 연결 관계 파악
    conjunction_check = modB.conjunction_association(summary4)
    # print(conjunction_check)

    # Final Score Evaluation
    reliability_2 = modB.evaluation_moduleB(sudden_leap_degree, conjunction_check, param_arrayB=[0.5,0.5,0])
    return reliability_2

# (3) Republishing Same Article Checker
# Functions Required::
# morpheme_separation() - 형태소를 분리하는 역할
# sql_republish_search() - 데이터베이스의 탐색
# make_summary() - 유사 기사를 요약하는 과정
# WordtoVec_exclusiveB() - 단어간의 연관성 계산
# make_keywordlist() - 기사의 주요단어 추출
# evaluation_moduleC() - 기사간 유사도 계산

def republishing_same_checker(summary5, reporter, press):
    morpheme_processed_A = modC.make_keywordlist(summary5)
    similar_article, reporter_score, press_score = modC.sql_republish_search(morpheme_processed_A, reporter, press)
    summarized_s_article = modC.make_summary(similar_article)
    morpheme_processed_B = modC.make_keywordlist(summarized_s_article)
    similarity = modC.WordtoVec_exclusiveB(morpheme_processed_A, morpheme_processed_B)
    # print(similarity)
    # print(reporter_score)
    # print(press_score)

    # Final Score Evaluation
    reliability_3 = modC.evaluation_moduleC(similarity, reporter_score, press_score, param_array=[0.3,0.3,0.3,10])
    return reliability_3

# [END Major Module]


# 세 가지 모듈에서 각 신뢰도가 계산되었으면, 마지막으로 최종 점수를 계산해주어야 한다.
# [START Manufacturing]
def manufacture_reliability(reliability_1, reliability_2, reliability_3, param_array):
    reliability_result = param_array[0]*reliability_1+param_array[1]*reliability_2+param_array[2]*reliability_3+param_array[3]
    return reliability_result
# [END Manufacturing]

# 웹페이지에 표시될 형태로 가공한다. 원래의 점수는 0~100으로 표현되었지만,
# 웹페이지에는 5단계의 구분으로 신뢰도가 표현될 것이다.
# Showing to the web
# [START Webbing]
def how_to_show_in_web(rel1, rel2, rel3, reliability_result):

    if rel1 <= 20: howtoshowinweb_1 = 1
    elif rel1 > 20 and rel1 <= 40: howtoshowinweb_1 = 2
    elif rel1 > 40 and rel1 <= 60: howtoshowinweb_1 = 3
    elif rel1 > 60 and rel1 <= 80: howtoshowinweb_1 = 4
    elif rel1 > 80: howtoshowinweb_1 = 5

    if rel2 <= 20: howtoshowinweb_2 = 1
    elif rel2 > 20 and rel2 <= 40: howtoshowinweb_2 = 2
    elif rel2 > 40 and rel2 <= 60: howtoshowinweb_2 = 3
    elif rel2 > 60 and rel2 <= 80: howtoshowinweb_2 = 4
    elif rel2 > 80: howtoshowinweb_2 = 5

    if rel3 <= 20: howtoshowinweb_3 = 1
    elif rel3 > 20 and rel3 <= 40: howtoshowinweb_3 = 2
    elif rel3 > 40 and rel3 <= 60: howtoshowinweb_3 = 3
    elif rel3 > 60 and rel3 <= 80: howtoshowinweb_3 = 4
    elif rel3 > 80: howtoshowinweb_3 = 5

    if reliability_result <= 20: howtoshowinweb_res = 1
    elif reliability_result > 20 and reliability_result <= 40: howtoshowinweb_res = 2
    elif reliability_result > 40 and reliability_result <= 60: howtoshowinweb_res = 3
    elif reliability_result > 60 and reliability_result <= 80: howtoshowinweb_res = 4
    elif reliability_result > 80: howtoshowinweb_res = 5

    return howtoshowinweb_1, howtoshowinweb_2, howtoshowinweb_3, howtoshowinweb_res
# [END Webbing]




# 이 구성만으로도 이미 가짜뉴스 판별의 역할을 할 수 있기 때문에, 전반적인 과정이 잘 작동하고 있는지 알아볼 필요가 있다.
# 백엔드 코드가 잘 작동하고 있는지 알아보기 위해 해당 파일을 가동시켜보자.
# if __name__ == '__main__':
#     link = 'https://www.yna.co.kr/view/AKR20210824098100051?section=society/all'
#     link = 'https://www.yna.co.kr/view/AKR20210827096200001?section=politics/all'

#     # Crawl title and body contents
#     press, reporter, articletitle, articlecontents = get_titleAndContents(link)
    
#     print(press)
#     print(reporter)
#     print(articletitle)
#     print(articlecontents)

#     # Make summary of contents
#     summary1 = get_summary(articletitle, articlecontents, 1)
#     summary2 = get_summary(articletitle, articlecontents, 2)
#     summary3 = get_summary(articletitle, articlecontents, 3)
#     summary4 = get_summary(articletitle, articlecontents, 4)
#     summary5 = get_summary(articletitle, articlecontents, 5)

#     print("\n\n------Summary 1------")
#     print(summary1)
#     print("\n\n------Summary 2------")
#     print(summary2)
#     print("\n\n------Summary 3------")
#     print(summary3)
#     print("\n\n------Summary 4------")
#     print(summary4)
#     print("\n\n------Summary 5------")
#     print(summary5)

#     print("\n\n\n------Reliabilities------")
#     # Running modules
#     reliability_1 = provocative_title_checker(articletitle, summary1, summary2)
#     print('reliability 1: '+str(reliability_1))
#     reliability_2 = publicity_article_checker(articletitle, summary3, summary4)
#     print('reliability 2: '+str(reliability_2))
#     reliability_3 = republishing_same_checker(summary5, reporter, press)
#     print('reliability 3: '+str(reliability_3))
#     # we need to train to make param_array
#     rel = manufacture_reliability(reliability_1, reliability_2, reliability_3, param_array=[0.3,0.3,0.3,0.1])
    
#     # Showing to the web
#     h1, h2, h3, h4 = how_to_show_in_web(reliability_1, reliability_2, reliability_3, rel)

#     print("------Web------")
#     print(rel)
#     print(h1)
#     print(h2)
#     print(h3)
#     print(h4)
