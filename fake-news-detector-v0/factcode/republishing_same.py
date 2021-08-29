# publicity_article.py
# Written by Byeongho Hwang (황병호)

# model_factcheck.py가 전반적인 기능을 크게 구현해놓은 연결이라고 한다면,
# republishing_same.py는 그 메이저 모듈 중 하나인 동일 기사 반복 게재 탐지 기능의
# 각 기능의 세부 기능과 흐름을 구현해놓은 것이다.

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause

# (3) Republishing Same Article Checker
# Functions Required::
# morpheme_separation - From modA
# sql_republish_search
# make_summary
# WordtoVec_exclusiveB
# make_keywordlist
# evaluation_moduleC

# sdk에서 url 배포를 위해 실행시킬 경우 아래 모듈을 사용, 위 모듈은 주석 처리
try:
    from factcode.CrawlMorpheme import crawlmorpheme
    from factcode.StringProcess import summaries
    from factcode import provocative_title
    from factcode.Optimization import sqlsearch
# 로컬 컴퓨터로 실행시킬 경우 위 모듈을 사용, 아래 모듈은 주석 처리
except:
    from CrawlMorpheme import crawlmorpheme
    from StringProcess import summaries
    import provocative_title
    from Optimization import sqlsearch

# from factcode.CrawlMorpheme import crawlmorpheme
# from factcode.StringProcess import summaries
# from factcode import provocative_title
# from factcode.Optimization import sqlsearch

cm = crawlmorpheme
pt = provocative_title
sr = summaries
sq = sqlsearch

# 데이터베이스에 접근해 언론사, 기자, 유사기사를 검색한다.
def sql_republish_search(keyword_array, personname, pressname):
    similar_article, reporter_score, press_score = sq.search(keyword_array, personname, pressname)
    return similar_article, reporter_score, press_score

# 원래도 기사를 요약했듯, 새롭게 검색된 기사 역시 요약한다.
def make_summary(text):
    summary = sr.rps_summary(text)
    return summary

# 유사 기사 본문과 원래 기사 본문의 유사도를 검색한다.
def WordtoVec_exclusiveB(morpheme1, morpheme2):
    similarity = cm.morpheme_model_BB(morpheme1, morpheme2)
    return similarity

# 자주 언급되는 단어의 리스트 추출
def make_keywordlist(text):
    arr = cm.often_top_n(text, n=10)
    return arr

# 동일 기사 반복 게재 점수 계산
def evaluation_moduleC(num1, num2, num3, param_array):
    reliability_3 = num1 * param_array[0] + num2 * param_array[1] + num3 * param_array[2] + param_array[3]
    return reliability_3

if __name__ == '__main__':
    query = 'https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=100&oid=001&aid=0012579586'
    articletitle, summary5, journalist = cm.crawl_navernews(query)
    press = 'naver'

    morpheme_processed_A = make_keywordlist(summary5)
    similar_article, reporter_score, press_score = sql_republish_search(morpheme_processed_A, journalist, press)
    summarized_s_article = make_summary(similar_article)
    morpheme_processed_B = make_keywordlist(summarized_s_article)
    similarity = WordtoVec_exclusiveB(morpheme_processed_A, morpheme_processed_B)

    # Final Score Evaluation
    reliability_3 = evaluation_moduleC(similarity, reporter_score, press_score, param_array=[0.3,0.3,0.3,0.1])
    print(reliability_3)