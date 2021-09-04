# causal.py
# Written by Yunji Lee (이윤지)

# causal.py는 명사간의 인과관계를 파악해 문장 내 도치 여부를 파악하는 파일이다.

# SPDX-FileCopyrightText: © 2021 Yunji Lee <qwerty5098@kyonggi.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause

from sklearn.feature_extraction.text import TfidfVectorizer

def comparison(morpheme1, morpheme2):
    
    print(type(morpheme1))
    print(type(morpheme2))

    for i in range(len(morpheme1)):
        print(type(morpheme1[i]))
        print(morpheme1[i])
        morpheme1[i] = str(morpheme1[i][0])
        print(morpheme1[i])
    for j in range(len(morpheme2)):
        morpheme2[j] = str(morpheme2[j][0])
    
    #string화
    s_morpheme1 = ",".join(str(i) for i in morpheme1)
    s_morpheme2 = ",".join(str(j) for j in morpheme2)

    print(type(s_morpheme1))
    print(type(s_morpheme2))

    morphemelist = []
    morphemelist.append(str(s_morpheme1))
    morphemelist.append(str(s_morpheme2))
    # morphemelist = [s_morpheme1, s_morpheme2]
    
    #TF-IDF값을 활용하여 유사도 계산
    tfidf_vectorizer=TfidfVectorizer(min_df=1)  
    tfidf_matrix=tfidf_vectorizer.fit_transform(morphemelist)
    
    mat_relation_similarity=(tfidf_matrix*tfidf_matrix.T)
    
    #float화
    relation_similarity=(round(float(mat_relation_similarity[0, 1]),2)*100)*10
    
    return relation_similarity


if __name__ == '__main__':
    morpheme1=['한미', '연합', '훈련', '연기', '예정', '시행', '규모', '축소']
    morpheme2=['국방부', '시기', '규모', '미확정', '협의', '사전', '준비', '착수', '한미', '연합', '훈련', '축소', '실시', 
                '전망', '정연주', '제작', '일러스트', '서울', '연합뉴스', '김', '기자', '여권', '일각', '한미', '연합', '훈련', 
                '연기론', '확산', '가운데', '한국', '미국', '군', '당국', '신종', '코로나바이러스', '감염증', '코로나', '상황', 
                '등', '고려', '규모', '축소', '실시', '전망', '국방부', '후반기', '훈련', '시기', '규모', '등', '확정', '양국', 
                '협의', '중이', '입장', '거듭', '부승찬', '국방부', '대변인', '정례', '브리핑', '관련', '질의', '하반기', '연합', 
                '훈련', '시기', '규모', '방식', '확정', '며', '한미', '이', '관련', '각종', '여건', '종합', '고려', '협의', '고', 
                '답', '한미', '군', '당국', '사전', '연습', '성격', '위기', '관리', '참모', '훈련', '후반기', '연합', '지휘', '훈련', 
                '각각', '진행', '일정', '훈련', '준비', '중인', '것', '앞서', '문재인', '대통령', '전날', '이번', '달', '예정', '한미', 
                '연합', '훈련', '관련', '여러', '가지', '고려', '미국', '측', '협의', '고', '말', '문', '대통령', '군', '주요', '지휘', 
                '관', '국방', '현안', '보고', '자리', '서욱', '국방부', '장관', '한미', '연합', '훈련', '관련', '현재', '코로나', '상황', 
                '등', '현실', '여건', '감안', '방역', '당국', '및', '미국', '측', '협의', '중', '보고', '언급', '청와대', '핵심', 
                '관계자', '전', '이', '범여', '의원', '여', '명', '연합', '훈련', '연기', '등', '연기론', '확산', '이', '군', '관계자', 
                '한미', '내주', '연습', '위', '토론', '전체', '훈련', '시나리오', '점검', '등', '훈련', '준비', '시작', '고', '전', 
                '다른', '관계자', '현재', '한미연합사령부', '합참', '등', '군', '내부', '분위기', '훈련', '쪽', '말', '군', '일각', 
                '한미', '군', '당국', '시작', '것', '예상', '훈련', '직전', '시기', '규모', '등', '대한', '발표', '것', '예상', '계획', 
                '일정', '훈련', '시작', '코로나', '확산', '세', '등', '고려', '규모', '축소', '훈련', '시설', '벙커', '여건', '밀', 
                '밀접', '밀집', '밀폐', '환경', '노출', '수', '참여', '인원', '대폭', '때문', '군', '관계자', '반기', '연합', '지휘', 
                '훈련', '수준', '예상', '고', '말']
    
    relation_similarity=comparison(morpheme1, morpheme2)
    
    print(relation_similarity)
