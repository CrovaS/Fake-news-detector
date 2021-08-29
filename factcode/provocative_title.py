# provocative_title.py
# Written by Byeongho Hwang (황병호)

# model_factcheck.py가 전반적인 기능을 크게 구현해놓은 연결이라고 한다면,
# provocative_title.py는 그 메이저 모듈 중 하나인 자극적인 제목 감지 기능의
# 각 기능의 세부 기능과 흐름을 구현해놓은 것이다.

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause

# (1) Provocative Title Checker
# Functions Required::
# morpheme_separation()
# causal_comparison()
# WordtoVec_exclusiveA()
# evaluation_moduleA()

# sdk에서 url 배포를 위해 실행시킬 경우 위 모듈을 사용
try:
    from factcode.CrawlMorpheme import crawlmorpheme
    from factcode.CrawlMorpheme import crawlbs
    from factcode.Optimization import causal
# 로컬 컴퓨터로 실행시킬 경우 아래 모듈을 사용
except:
    from CrawlMorpheme import crawlmorpheme
    from CrawlMorpheme import crawlbs
    from Optimization import causal

# from factcode.CrawlMorpheme import crawlmorpheme
# from factcode.CrawlMorpheme import crawlbs
# from factcode.Optimization import causal

cm = crawlmorpheme
cb = crawlbs
cs = causal

# 형태소 감지기
def morpheme_separation(text):
    morpheme_array = cm.get_morpheme(text)
    return morpheme_array

# 조사 비교를 통한 자극적 도치 가능성 판별
def causal_comparison(morpheme1, morpheme2):
    relation_similarity = cs.comparison(morpheme1, morpheme2)
    return relation_similarity

# 제목과 본문에서 자주 언급되어 있는 가져온 뒤, 
# 제목이 실제로 본문을 요약하고 있는 것인지 점수로 표시
def WordtoVec_exclusiveA(title, text):
    title_list = cm.often_top_n(title)
    article_list = cm.often_top_n(text)
    result = cm.morpheme_model_AA(title_list, article_list)
    return result

# 파라미터 배열을 가져와 최종 점수 계산
def evaluation_moduleA(num1, num2, param_arrayA):
    reliability_1 = num1 * param_arrayA[0] + num2 * param_arrayA[1] + param_arrayA[2]
    return reliability_1

if __name__ == '__main__':
    import sys
    print(sys.version)
    
    # 각 웹페이지의 형태가 항상 바뀌므로 크롤러가 정상 작동하지 않을 수 있다.
    query = 'https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=100&oid=001&aid=0012579586'
    articletitle, summary1, journalist = cm.crawl_news(query)

    # Causal Relationship Comparison
    morpheme1 = morpheme_separation(articletitle)
    morpheme2 = morpheme_separation(summary1)
    relation_similarity = causal_comparison(morpheme1, morpheme2)

    # Word2Vec AI Model
    WordtoVec_result = WordtoVec_exclusiveA(articletitle, summary1)

    # Final Score Evaluation
    reliability_1 = evaluation_moduleA(relation_similarity, WordtoVec_result, param_arrayA=[0,1,0])
    print (journalist)
    print(reliability_1)