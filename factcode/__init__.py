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

# factcode 폴더는 크게 두 가지로 나눠져 있다.
# 첫째는 가짜뉴스를 판별하는 부분이며, 둘째는 서비스 전반을 구성하는 부분이다.
#
# 가짜뉴스 판별: CrawlMorpheme, Optimization, PositivityCheck, StringProcess (폴더)
#               model_factcheck.py, provocative_title.py, publicity_article.py,
#               republishing_same.py, stringbox.py (파일)
# 서비스 전반: static, templates (폴더)
#               crud.py, model_cloudsql.py (파일)
# 
# 현재 파일 자체에서는 crud.py에서 html의 url에 따른 페이지를 맡고있어 crud.py의 작동에
# 가장 큰 초점을 맞추고 있다.

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause


import logging

from flask import current_app, Flask, redirect, url_for


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        model = get_model()
        model.init_app(app)

    # Register the Factchecker CRUD blueprint.
    from .crud import crud
    app.register_blueprint(crud, url_prefix='/factchecker')

    # Add a default root route.
    @app.route("/")
    def index():
        return redirect(url_for('crud.list'))

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app


def get_model():
    model_backend = current_app.config['DATA_BACKEND']
    if model_backend == 'cloudsql':
        from . import model_cloudsql
        model = model_cloudsql
    else:
        raise ValueError(
            "No appropriate databackend configured. "
            "Please specify datastore, cloudsql, or mongodb."
            "When using Fact checker, it must be cloudsql.")

    return model
