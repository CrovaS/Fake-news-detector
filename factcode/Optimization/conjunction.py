# conjunction.py
# Written by Subin Kim (김수빈)

# conjunction.py는 문장 내 접속사를 이용해 분위기 전환 정도를 파악하는 파일이다.
# 

# SPDX-FileCopyrightText: © 2021 Subin Kim <subinga18@naver.com>
# SPDX-License-Identifier: BSD-3-Clause

def check(text):
    conjunction_check = 0.5
    return conjunction_check

# 순접 : 그리고, 게다가, 더욱이, 더구나,뿐만 아니라, 동시에, 그런 점에서
# 인과 : 그러므로, 따라서, 그러니까, 그리하여, 그렇게, 때문에, 그래서, 그러면, 그러니
# 보완 : 즉, 곧, 예를 들면, 사실상
# 종결 : 결국, 결론적으로

# 역접 : 그러나, 하지만, 그렇지만, 그럼에도, 반면에, 오히려, 반대로
# 전환 : 그런데, 다른 한편, 다만, 바꿔 말하면


# summaries 완료 되면 article 아닌 sum 쓰기
# 순접,인과,보완,종결 : 1 / 역접,전환 : 0
def conj(article):
    
    state = 0.5
    same =['이어','그리고','게다가','더욱이','더구나''뿐만 아니라','동시에','그런 점에서'
    ,'그러므로','따라서','그러니까','그리하여','그렇게','때문에','그래서','그러면','그러니'
    ,'즉','곧','예를 들면','사실상'
    ,'결국','결론적으로']

    differ = ['그러나','하지만','그렇지만','그럼에도','반면에','오히려','반대로','그런데','다른 한편','다만','바꿔 말하면']

    #list_same = [i for i in range(len(article)) for j in range(len(same)) if same[j] in article[i]]
   
    #print (list_same)

    for i in range(len(article)):
        for j in range(len(same)):
            if same[j] in article[i]:
                state = 1
                list_same=[i]
        
        for j in range(len(differ)):
            if differ[j] in article[i]:
                state = 0
                list_differ=[i]

    print(state)
    print('same이 들어간 list 번호: ',list_same)
    print('differ이 들어간 list 번호: ',list_differ)

    return state
    
    
if __name__ == '__main__':
    query = input ('기사 링크를 입력하세요 : ')
    title ,article,journalist = crawl_news(query)
    conj(article)