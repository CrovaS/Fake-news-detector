# sqlsearch.py
# Written by Yunji Lee (이윤지)
# Editted by Byeongho Hwang (황병호)

# sqlsearch.py는 데이터베이스에 접근해 기사, 언론사, 유사 기사 정보를 얻는 과정을 수행한다.
# 등등등...

# SPDX-FileCopyrightText: © 2021 Yunji Lee <qwerty5098@kyonggi.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause

def rpt_score(data1, data2):
    if data1 == 0: result = -1
    else: result = 20*data2/data1
    return result

def prs_score(data1, data2):
    if data1 == 0: result = -1
    else: result = 20*data2/data1
    return result

def search(keyword_array, personname, pressname):
    import pymysql

    connect = pymysql.connect(host='34.64.153.163', user='root', password='passw0rd', db='factchecker', charset='utf8mb4')
    cur = connect.cursor()

    keyword_plusarray = []
    for keyword in keyword_array:
        keyword_plus = keyword + ';'
        keyword_plusarray.append(keyword_plus)

    # keyword searching query
    # 아래 식을 만들기 위해 for문을 사용한다.
    # query_key ="((REPLACE((...),'noun8','noun8_plus')),'noun9','noun9_plus'))"
    query_key = ""
    if keyword_array == []: query_key = "content"
    else:
        for i in range(len(keyword_array)):
            if i == 0: query_key = "(REPLACE(content, '" + keyword_array[i] + "', '" + keyword_plusarray[i] + "'))"
            else: query_key = "(REPLACE(" + query_key + ", '" + keyword_array[i] + "', '" + keyword_plusarray[i] + "'))"
    query_keyword = "SELECT content FROM newsbox ORDER BY (((LENGTH(" + query_key + ")) - LENGTH(content))/LENGTH(';')) DESC LIMIT 1"

    data_keyword = cur.execute(query_keyword)
    connect.commit()
    data_keyword = cur.fetchmany(size=1)
    data_keyword = data_keyword[0][0]
    print(data_keyword)

    # reporter reliablity query
    query_reporter1 = "SELECT COUNT(*) FROM newsbox WHERE (reporter = '" + personname + "')"
    data_reporter1 = cur.execute(query_reporter1)
    connect.commit()
    data_reporter1 = cur.fetchmany(size=1)
    data_reporter1 = data_reporter1[0][0]

    query_reporter2 = "SELECT SUM(rel3) FROM newsbox WHERE (reporter = '" + personname + "')"
    data_reporter2 = cur.execute(query_reporter2)
    connect.commit()
    data_reporter2 = cur.fetchmany(size=1)
    data_reporter2 = data_reporter2[0][0]

    # pressname reliability query
    query_press1 = "SELECT COUNT(*) FROM newsbox WHERE (reporter = '" + pressname + "')"
    data_press1 = cur.execute(query_press1)
    connect.commit()
    data_press1 = cur.fetchmany(size=1)
    data_press1 = data_press1[0][0]

    query_press2 = "SELECT SUM(rel3) FROM newsbox WHERE (reporter = '" + pressname + "')"
    data_press2 = cur.execute(query_press2)
    connect.commit()
    data_press2 = cur.fetchmany(size=1)
    data_press2 = data_press2[0][0]

    if data_reporter2 == 'None': data_reporter2 = 0
    if data_press2 == 'None': data_press2 = 0

    similar_article = data_keyword
    reporter_score = rpt_score(data_reporter1, data_reporter2)
    press_score = prs_score(data_press1, data_press2)

    return similar_article, reporter_score, press_score


if __name__ == '__main__':
    keyword_array = ['한미연합', '훈련', '국방부', '기동대', '27사단', '대통령', '문재인', '트럼프', '미국연방', '북한']
    personname = '황병호'
    pressname = '네이버'
    similar_article, reporter_score, press_score = search(keyword_array, personname, pressname)
