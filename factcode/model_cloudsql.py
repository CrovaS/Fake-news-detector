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

# model_cloudsql.py에서는 어떤 데이터베이스를 필요로 하는지 알아보고, 접근을 진행한다.
# 구체적인 기능들을 구현하기 시작하며, 첫 리스트의 데이터베이스를 구축하는 동시에
# 가짜뉴스 판별기로의 연결을 시도하는 함수도 존재한다.

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
try:
    from factcode import model_factcheck
except:
    import model_factcheck

# from factcode import model_factcheck

factcheck = model_factcheck

builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START model]
class BestArticle(db.Model):
    __tablename__ = 'bestarticles'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    date = db.Column(db.String(16))
    press = db.Column(db.String(32))
    reporter = db.Column(db.String(64))
    title = db.Column(db.String(128))

    def __repr__(self):
        return "<Article(title='%s', reporter=%s)" % (self.title, self.reporter)
# [END model]


class Article(db.Model):
    __tablename__ = 'newsbox'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    date = db.Column(db.String(16))
    press = db.Column(db.String(32))
    reporter = db.Column(db.String(64))
    title = db.Column(db.String(128))
    content = db.Column(db.String(20000))
    rel1 = db.Column(db.Integer)
    rel2 = db.Column(db.Integer)
    rel3 = db.Column(db.Integer)
    reliability = db.Column(db.Integer)

    def __repr__(self):
        return "<Article(title='%s', reporter=%s)" % (self.title, self.reporter)
# [END model]


# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (BestArticle.query
             .order_by(BestArticle.id)
             .limit(limit)
             .offset(cursor))
    books = builtin_list(map(from_sql, query.all()))
    print(str(books))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)
# [END list]

# [START factchecking]
def factchecking(link):
    print(link)
    # 링크로부터 언론사, 기자, 제목, 본문 크롤링
    press, reporter, articletitle, articlecontents = factcheck.get_titleAndContents(link)
    
    # 분석을 위한 다섯 가지 요약본 준비
    summary1 = factcheck.get_summary(articletitle, articlecontents, classification=1)
    summary2 = factcheck.get_summary(articletitle, articlecontents, classification=2)
    summary3 = factcheck.get_summary(articletitle, articlecontents, classification=3)
    summary4 = factcheck.get_summary(articletitle, articlecontents, classification=4)
    summary5 = factcheck.get_summary(articletitle, articlecontents, classification=5)

    # 주어진 정보를 세 개의 모델로 투입, 각 신뢰도를 얻어냄
    reliability_1 = factcheck.provocative_title_checker(articletitle, summary1, summary2)
    reliability_2 = factcheck.publicity_article_checker(articletitle, summary3, summary4)
    reliability_3 = factcheck.republishing_same_checker(summary5, reporter, press)
    
    # 최종 신뢰도 계산 (param_array의 학습이 필요함)
    reliability_result = factcheck.manufacture_reliability(reliability_1, reliability_2, reliability_3, param_array=[0.3,0.3,0.3,10])
    
    # 웹페이지에 표시할 정보로 변환
    howtoshowinweb1, howtoshowinweb2, howtoshowinweb3, howtoshowinweb_res = factcheck.how_to_show_in_web(reliability_1, reliability_2, reliability_3, reliability_result)

    return howtoshowinweb1, howtoshowinweb2, howtoshowinweb3, howtoshowinweb_res
# [END factchecking]

# 앱이 시작되면 해당 함수가 작동함.
# 데이터베이스로부터 테이블이 무사히 만들어지면 'All tables created'라는 문구 출력
def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
