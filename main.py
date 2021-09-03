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

# 메인 코드는 전체 코드를 작동시키기 위한 트리거다.
# config.py를 통해 Google Cloud Platform의 데이터베이스 접근 권한을 얻어온 뒤,
# 전반적인 기능을 담당하는 폴더 factcode를 작동시켜 전체 동작이 이루어지도록 한다. 

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause

import factcode
import config


app = factcode.create_app(config)


# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
