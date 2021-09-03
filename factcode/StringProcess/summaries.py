# coding:utf-8
# 1번 줄의 주석은 주석이 아닌 코드의 부분으로, 지우면 코드가 작동하지 않으므로 주의.

# summaries.py
# Written by Hanna Jeon (전한나)

# summaries.py는 본문을 그대로 가져와 처리할 때 너무 많은 시간이 소요될 경우,
# 본문을 요약해 시간을 단축하기 위한 함수들을 저장한 파일이다.

# SPDX-FileCopyrightText: © 2021 Hanna Jeon <jhn90928@gmail.com>
# SPDX-License-Identifier: BSD-3-Clause

def sum1(title, content):
    summary = content
    return summary

def sum2(title, content):
    summary = content
    return summary

def sum3(title, content):
    summary = ''
    paragraph_list = content.split('\n')
    for paragraph in paragraph_list:
        sentence_list = []
        sentence_list_mft = paragraph.split('. ')
        for sentence in sentence_list_mft:
            if len(sentence) > 3: sentence_list.append(sentence)
        if len(sentence_list) == 0: paragraph_summary = ''
        elif len(sentence_list) <= 2: paragraph_summary = paragraph + '\n'
        else: paragraph_summary = sentence_list[0] + ". " + sentence_list[-1] + '\n'
        if len(paragraph) < 2: paragraph_summary = ''
        summary = summary + paragraph_summary
    return summary

def sum4(title, content):
    summary = ''
    paragraph_list = content.split('\n')
    for paragraph in paragraph_list:
        sentence_list = []
        sentence_list_mft = paragraph.split('. ')
        for sentence in sentence_list_mft:
            if len(sentence) > 3: sentence_list.append(sentence)
        if len(sentence_list) == 0: paragraph_summary = ''
        elif len(sentence_list) == 1: paragraph_summary = paragraph + '\n'
        else: paragraph_summary = sentence_list[0] + '.\n'
        if len(paragraph) < 2: paragraph_summary = ''
        summary = summary + paragraph_summary
    return summary

def sum5(title, content):    
    from gensim.summarization.summarizer import summarize #gesnim 라이브러리 이용해서 기사 요약

    snews_contents = summarize(content)
    summary = snews_contents

    return summary

def rps_summary(content):

    from gensim.summarization.summarizer import summarize #gesnim 라이브러리 이용해서 기사 요약

    snews_contents = summarize(content)
    summary = snews_contents
    text = summary
    return text

if __name__ == '__main__':

    title = '"아기라도 살려주세요"…철조망 너머로 아기 던지는 절박한 아프간 엄마들'

    content = '''높이가 3m 이상 돼 보이는 날카로운 철조망 너머로 아기가 아슬아슬하게 넘어간다. 작은 몸집의 아기가 혹여나 철조망에 걸린다면 목숨까지 위태로울 수 있다. 이처럼 위험천만한 일을 벌이는 이는 다름 아닌 아기의 엄마다. 엄마들은 “아이를 살려달라”며 울부짖고, 군인들은 아기들을 조심스럽게 받으며 눈물을 삼킨다. 이슬람 무장조직 탈레반에 장악된 아프가니스탄의 처절한 현장이다.
아프간 수도 카불에서 탈출 길이 막히면서 자식이라도 살리려는 엄마들이 아기를 철조망 너머로 던지며 생이별을 택하는 일이 일어나 주위를 안타깝게 하고 있다. 19일(현지시간) 영국 일간 인디펜던트 등 외신에 따르면 이날 트위터 등 소셜미디어(SNS)에는 일부 아기 엄마들이 철조망 너머의 영국군에게 아이를 던지는 영상이 공개됐다.
인디펜던트에 따르면 영상 속 장소는 영국이 자국민과 관계자들을 탈출시키기 위해 공수부대원들이 지키도록 한 하미드 카르자이 국제공항 근처의 바론 호텔이다. 탈레반의 압제를 우려한 아프간인들은 영국군이 경비를 서고 있는 이곳에 몰려들어 구조를 요청했다.

영상에는 “아기라도 살려달라”는 외침 속에 던져진 아기들을 영국 군인이 운 좋게 손으로 받아내는 모습이 나온다. 당시 현장에 있던 영국군 관계자는 인디펜던트와의 인터뷰에서 “아프간 어머니들은 탈레반에 구타를 당하고 있었다”며 “그들은 폭행을 당하면서도 ‘내 아기만이라도 살려달라’고 소리치며 철조망 반대편에 있는 우리에게 아기를 던졌다”고 밝혔다.
그는 이어 “던져진 아기 몇 명은 철조망 위에 떨어졌고, 그 후 일어난 일은 끔찍했다”며 “밤이 끝날 무렵까지 모든 부대원이 눈물을 흘렸다”고 말했다.
또 다른 영상에서도 영국군이 지키는 한 호텔 철조망 앞에 모인 군중들이 머리 위로 갓난아기를 옮기는 모습이 포착됐다. 카불 공항에서도 마찬가지로 아프간 시민들이 자신의 아이라도 먼저 대피시키고자 공항 벽 너머의 미군에게 아이를 보내는 경우도 있었다.
뉴욕타임스(NYT) 등 외신에 따르면 카불 공항 주변엔 아프간을 탈출하려는 수천명의 인파가 몰려들었으며, 공항 출입구를 장악한 탈레반이 이들을 해산시키기 위해 총을 쏘고 폭력을 행사하면서 부상자와 사망자가 속출하는 것으로 전해졌다.'''

    sum_1 = sum1(title, content)
    sum_2 = sum2(title, content)
    sum_3 = sum3(title, content)
    sum_4 = sum4(title, content)
    sum_5 = sum5(title, content)
    sum_rps = rps_summary(content)

    print("---Summary 1---\n")
    print(sum_1)
    print("\n")
    print("---Summary 2---\n")
    print(sum_2)
    print("\n")
    print("---Summary 3---\n")
    print(sum_3)
    print("\n")
    print("---Summary 4---\n")
    print(sum_4)
    print("\n")
    print("---Summary 5---\n")
    print(sum_5)
    print("\n")
    print("---Summary RPS---\n")
    print(sum_rps)
    print("\n")