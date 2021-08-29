# sudden.py
# Written by Byeongho Hwang (황병호)

# sudden.py는 분석된 정보들을 이용해 홍보성 기사일 가능성을 계산한다.

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause

def decide_type(pos_title, pos_summary):
    pos = 0
    count = 0
    for i in pos_summary:
        count = count + 1
        pos = pos + i
    pos_sum = float(pos/count)

    if pos_title > 0 and pos_sum > 0: return 1
    if pos_title == 0 and pos_sum > 0: return 2
    if pos_title < 0 and pos_sum > 0: return 3
    if pos_title > 0 and pos_sum == 0: return 4
    if pos_title == 0 and pos_sum == 0: return 5
    if pos_title < 0 and pos_sum == 0: return 6
    if pos_title > 0 and pos_sum < 0: return 7
    if pos_title == 0 and pos_sum < 0: return 8
    if pos_title < 0 and pos_sum < 0: return 9
    return 0


def check_there(noun, content):
    which_paragraph_has_the_pnoun = []
    paragraph_number = 1
    for paragraph in content:
        if noun in paragraph: which_paragraph_has_the_pnoun.append(paragraph_number)
        paragraph_number = paragraph_number + 1
    return which_paragraph_has_the_pnoun


def first_leap_calculation(title_propernoun_leap, max_leap,checker):
    leap_degree = 0
    if checker == 1: leap_degree = (title_propernoun_leap + max_leap/2)
    if checker == 0: leap_degree = 2*(title_propernoun_leap + max_leap/2)
    return leap_degree


def second_leap_calculation(sudden_leap_degree, mode):
    
    leap_degree = sudden_leap_degree

    if mode == 1: # 제목 긍정, 기사 긍정 -> 100% 반영
        leap_degree = sudden_leap_degree * 1.0
    if mode == 2: # 제목 중립, 기사 긍정 -> 80% 반영
        leap_degree = sudden_leap_degree * 0.8
    if mode == 3: # 제목 부정, 기사 긍정 -> 80% 반영
        leap_degree = sudden_leap_degree * 0.8
    if mode == 4: # 제목 긍정, 기사 중립 -> 100% 반영
        leap_degree = sudden_leap_degree * 1.0
    if mode == 5: # 제목 중립, 기사 중립 -> 50% 반영
        leap_degree = sudden_leap_degree * 0.5
    if mode == 6: # 제목 부정, 기사 중립 -> 30% 반영
        leap_degree = sudden_leap_degree * 0.3
    if mode == 7: # 제목 긍정, 기사 부정 -> 100% 반영
        leap_degree = sudden_leap_degree * 1.0
    if mode == 8: # 제목 중립, 기사 부정 -> 10% 반영
        leap_degree = sudden_leap_degree * 0.1
    if mode == 9: # 제목 부정, 기사 부정 -> 30% 반영
        leap_degree = sudden_leap_degree * 0.3
    
    return leap_degree

def leap(pos_title, pos_summary, arr_title, arr_content):
    sudden_leap_degree = -1

    # Decide type
    art_type = decide_type(pos_title, pos_summary)

    # Search propernoun which is in title first
    title_propernoun_leap = 0
    checked_p = ''
    for pnoun in arr_title:
        check_in_there = check_there(pnoun, arr_content)
        if check_in_there == []:
            scaled_leap = 0
        else:
            pos_pyes = 0
            pos_pno = 0
            paragraph_count_pyes = 0
            paragraph_count_pno = 0
            total = len(pos_summary)
            
            for i in range(total):
                j = i + 1
                if j in check_in_there:
                    paragraph_count_pyes = paragraph_count_pyes + 1
                    pos_pyes = pos_pyes + pos_summary[i]
                else:
                    paragraph_count_pno = paragraph_count_pno + 1
                    pos_pno = pos_pno + pos_summary[i]
            if paragraph_count_pyes == 0: pyes = 0
            else: pyes = pos_pyes/paragraph_count_pyes
            if paragraph_count_pno == 0: pno = 0
            else: pno = pos_pno/paragraph_count_pno
            scaled_leap = 50*(pyes-pno)+50
        if title_propernoun_leap < scaled_leap:
            title_propernoun_leap = scaled_leap
            checked_p = pnoun

    # Search by leap scale
    leap_arr = []
    for i in range(len(pos_summary)-1):
        j = i + 1
        pos_leap = pos_summary[j] - pos_summary[i]
        leap_arr.append(pos_leap)
    max_leap = max(leap_arr)
    checked_a = []
    for i in range(len(pos_summary)-1):
        j = i + 1
        if max_leap == leap_arr[i]: checked_a.append(arr_content[j])
    checking = check_there(checked_p, checked_a)
    if checking == []: checker = 1
    else: checker = 0

    print(title_propernoun_leap)
    print(max_leap)
    print(checker)

    sudden_leap_degree = first_leap_calculation(title_propernoun_leap, max_leap, checker)
    sudden_leap_degree = second_leap_calculation(sudden_leap_degree, art_type)

    return sudden_leap_degree

if __name__ == '__main__':
    pos_title = -1
    pos_summary = [0.1, 0.2, 0.1]
    arr_title = ['맘스터치', '버거킹']
    arr_title = []
    arr_content = [['맘스터치'], ['맘스터치', '한국소비자원', '한국소비자센터'], ['맘스터치', '버거킹']]
    
    degree = leap(pos_title, pos_summary, arr_title, arr_content)
    print(degree)