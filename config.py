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

# config.py는 데이터베이스의 위치정보 등을 google cloud platform으로 전송해
# 접근 권한을 얻음과 동시에 어떤 데이터베이스의 정보를 필요로 하는지 알린다.
# 접근하고자 하는 데이터베이스, 사용자, 그리고 아이디 정보를 적어줘야한다.
# 어떤 유형의 베이스를 얻어올 수 있는지 또한 설정 가능한데,
# 모든 기능을 작동시키기 위해서는 cloudsql(기본 설정)으로 해야한다.

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause


import os

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY = 'secret'

# There are three different ways to store the data in the application.
# You can choose 'datastore', 'cloudsql', or 'mongodb'. Be sure to
# configure the respective settings for the one you choose below.
# You do not have to configure the other data backends. If unsure, choose
# 'datastore' as it does not require any additional configuration.

# ** IMPORTANT **
# However, This needs to be 'cloudsql' for fact-checker configuration.
DATA_BACKEND = 'cloudsql'

# Google Cloud Project ID. This can be found on the 'Overview' page at
# https://console.developers.google.com
PROJECT_ID = 'fake-news-base'

# CloudSQL & SQLAlchemy configuration
# Replace the following values the respective values of your Cloud SQL
# instance.
CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'passw0rd'
CLOUDSQL_DATABASE = 'factchecker'
# Set this value to the Cloud SQL connection name, e.g.
#   "project:region:cloudsql-instance".
# You must also update the value in app.yaml.
CLOUDSQL_CONNECTION_NAME = 'fake-news-base:asia-northeast3:fakenews'

# The CloudSQL proxy is used locally to connect to the cloudsql instance.
# To start the proxy, use:
#
#   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
#
# Port 3306 is the standard MySQL port. If you need to use a different port,
# change the 3306 to a different port number.

# Alternatively, you could use a local MySQL instance for testing.
LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

# When running on App Engine a unix socket is used to connect to the cloudsql
# instance.
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI

# Mongo configuration
# If using mongolab, the connection URI is available from the mongolab control
# panel. If self-hosting on compute engine, replace the values below.
MONGO_URI = \
    'mongodb://user:password@host:27017/database'
