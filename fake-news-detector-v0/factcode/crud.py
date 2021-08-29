# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Original by Google Inc.,
# Editted by Byeongho Hwang (황병호)

# crud.py에서는 url에 따라 어떤 정보를 표시해야하는 지 
# 구분해 그에 따른 정보를 불러오도록 명령한다.
# 현재 페이지는 두 가지 밖에 표시되지 않으며, 
# 필요한 확장 기능에 따라 url을 배정해 추가 기능 구현

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause


from factcode import get_model
from flask import Blueprint, redirect, render_template, request, url_for

crud = Blueprint('crud', __name__)

# ------------ base ------------
# 기본 url로, 처음 접속하게 되면 표시되는 페이지다.
@crud.route("/")
def list():
    
    # 페이지 토큰 받아오기
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    
    # 데이터베이스에서 요구하는 기본 리스트 정보 받아오기
    bestarticles, next_page_token = get_model().list(cursor=token)
    
    # html template 렌더링
    return render_template(
        "list.html",
        barticles=bestarticles,
        next_page_token=next_page_token)

# ------------ factcheck ------------
# 검색 후 나타나게 되는 url로, 기본 화면에 검색 결과를 나타내는 페이지다.
@crud.route('/factchecked/')
def factchecking():

    # 입력된 링크 정보 받아오기
    link = request.args.get('link')
    print(link)

    # 페이지 토큰 받아오기
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    
    # 가짜뉴스 판별 결과 가져오기
    rel1, rel2, rel3, relf = get_model().factchecking(link)
    # rel1 = 1
    # rel2 = 1
    # rel3 = 1
    # relf = 1
    # print(rel1)
    # print(rel2)
    # print(rel3)
    # print(relf)

    # html template 렌더링
    return render_template(
        "list.html",
        reliability_1=rel1,
        reliability_2=rel2,
        reliability_3=rel3,
        reliability_final=relf)

