<p align="center">
    <img src="https://user-images.githubusercontent.com/38221941/131619091-4c427677-e561-4fad-b95d-c156cf67e1b5.png" width="300px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>

<h1 align="center">Fake-news-detector</h1>


<p align="center">
   Disfactch 어쩌구....
</p>

## Preview
<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131960063-9d5248d5-4c2d-4263-b275-31179e203d2a.PNG" width="1000px">
</p>
<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131960100-94f1740b-aa8d-46da-a61e-353f3cda6292.PNG" width="1000px">
</p>
<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131960285-54903538-1d3b-48bf-8194-413eadb03fb0.PNG" width="1000px">
</p>



## Developer
2021 공개 sw 개발자 대회 
|Name|<a href="https://github.com/CrovaS">Byeongho Hwang<a>|<a href="https://github.com/subinga18">Subin Kim</a>|<a href="https://github.com/yunzi125">Yunji Lee</a>|<a href="https://github.com/jhn90928">Hanna Jeon</a>|
|:--|:--:|:--:|:--:|:--:|
|**Role**|Sudden<br>SQL Search<br>Function Gathering<br>webpage|Conjunction<br>Crawling(bs)<br>Word2Vec|Causal<br>Propernoun|Summaries<br>Positivity Check|


## Function
 - news factchecking 
 - 어쩌구 아직 덜 썼다 

## Structure
웹을 통해 기사의 링크를 입력할 수 있으며, 그에 따라 신뢰도가 출력되는 기능을 가지고 있다. flask를 이용해 HTML5와 python을 연동하며, 이는 인공지능 라이브러리 tensorflow를 보다 효과적으로 이용하기 위함이다.
<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131956906-14cb2bc1-8313-4397-b818-5a013474ad57.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>

가짜뉴스 판별 시스템 내부는 다음과 같이 구성되어 있다.
<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131956983-c0b4be2e-9bbf-43ab-a3eb-1a2a3e296edd.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>

기사 정보가 유입되면 전처리기에서 제목, 본문, 기자 정보 및 언론사 정보를 추출한다. 추출된 정보는 세 개의 시스템에 유입되며, 각 시스템은 각각의 점수를 산정해 최종적으로 점수 종합 시스템에 각 시스템 점수를 인풋으로 넣는다.

각 시스템은 낚시성 기사 제목 판별 시스템, 홍보성 기사 판별 시스템, 동일 기사 반복 게재 판별 시스템이다. 내부는 인공지능 모듈, 최적화 모듈, 그리고 일반 모듈로 이루어져 있다. 인공지능 모듈은 인공지능을 이용해 학습시키고, 각 요소들을 분류해내는 역할을 한다. 최적화 모듈은 상황에 맞추어 프로그래밍이 필요한 부분으로, 인공지능을 필요로 하지는 않으나 상세한 경우의 설정과 모델 설계가 필요한 부분이다. 마지막으로 일반 모듈은 하나의 함수와 같은 역할로, 어떤 인풋을 다른 모듈이 가공할 수 있도록 만들어주는 역할을 수행한다.
   
    
### System 1: 낚시성 기사 제목 판별
<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131957025-9fe94e04-8d39-4ac9-9156-ae6affad5004.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>
낚시성 제목을 판별하기 위해 크게 두 가지 요소를 이용한다.
 a) 핵심 문단의 문장 내 주요 단어들의 연관 정도가 얼마나 되는가?
 b) 제목의 단어간 인과관계와 기사의 단어간 인과관계가 유사한가?
 주요 단어들이 밀접하게 연관되어 있어야 기사의 신뢰성이 높다고 판단하며, 제목이 은연 중 인과를 바꾸어 자극적인 기사를 냈을 가능성을 판별하기 위해 제목의 인과와 기사의 인과를 비교해 얼마나 유사한지를 측정하게 된다.
    
    
### System 2: 홍보성 기사 판별
<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131957098-9fddefb4-6fb3-4ff8-b257-ddbe718782de.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>
기사 흉내를 내며 특정 상품을 홍보 하는 등의 기사또한 일종의 가짜뉴스로 판단했다. 실제로 홍보성 뉴스는 근거없이 특정 기업의 상품을 홍보한 뒤, 서술된 홍보성 작문이 입증된 효과나 반응인 것처럼 서술하는 경우가 있다. 따라서 이를 판별하기 위해서는 다음을 파악해 보아야한다.
 a) 문장, 문단의 맥락에 맞지 않게 갑작스러운 기업/기관 언급과 분위기의 도약이 있는가?
우선 input으로부터 제목, 본문요약 3, 본문요약 4를 가져온다. 본문의 요약은 본문 문단 분리, 중요성분 추출 등으로 만든다.
        
              
### System 3: 동일 기사 반복 게재
<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131957138-f7e09e03-163e-49d0-9a0c-a22fcfdae4e3.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>
동일 기사를 반복 게재하는 것은 다른 기사를 베껴 조회수를 올리기 위한 목적으로 주로 행해지며, 심지어 추가 정보 없이 기존의 기사를 축약한 형태로 만들어진다. 유사한 기사라고 하더라도 그것이 가짜뉴스로 보기는 어려운 경우가 많지만, 시간의 비교와 함께 너무 과도하게 축약되어 있는 경우 이를 가짜뉴스로 분류할 수 있어야한다. 또한 하루에 비정상적으로 많은 뉴스를 작성하는 기자, 제목과 본문이 다른 기사를 쓰는 언론사는 가짜뉴스를 판별하는데  반드시 살펴봐야할 대상이다. 따라서 다음 세 가지 요소를 살핀다.
 a) 기존의 기사를 짜집기한 요약본에 해당하는가?
 b) 기자가 하루에 비정상적으로 많은 기사를 올리는가?(하루에 1000개 이상의 기사를 올리는 기자도 있다.)
 c) 언론사에서 낚시성 기사를 주로 생산하는가?
이를 살펴보기 위해 우선 input으로부터 제목, 본문요약 5, 기자, 언론사를 가져온다. 여기서 제목과 본문요약 5의 내용에서 형태소를 분리하여 제목과 본문의 연관성을 조사하기 용이하게 한다.
        
        
### 모듈 정리
각 시스템에 필요한 모듈은 다음과 같이 정리된다.
<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131957176-16a807fd-00a9-4c39-bc72-234df00d12fa.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>

## Work Flow
### STEP 1: Google Cloud Platform Settings
1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Install Anaconda: https://www.anaconda.com/products/individual-d
3. (Optional) Create database in Google Cloud SQL
4. (Optional) Edit database, sql, python files in (config.py, app.yaml, tox.ini)


### STEP 2: Install Requirements
1. On Anaconda Prompt (Anaconda3)
```
conda create -n [Your name for environment] python=[Your python version] anaconda
```
For example,
```
conda create -n factchecker python=3.6.13 anaconda
```
2. Find your directory to this project
3. Install requirements
```
pip install -r requirements.txt
```


### STEP 3: KoNLPy, WordtoVec Settings
1. Install chrome driver for your version: https://chromedriver.chromium.org/downloads
2. Install ko.bin, ko.tsv here: https://github.com/Kyubyong/wordvectors
3. Put your chrome driver .exe file to
```
.../selenium
```
4. Put your ko.bin, ko.tsv file to
```
.../factcode/CrawlMorpheme/content
```
5. Make JAVA HOME Settings for usual KoNLPy settings (Environmental Variables)
6. Install JPype that fits your python: https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype , do the pip installation
```
pip install [Your Jpype filename]
```
For example,
```
pip install JPype1‑1.3.0‑cp310‑cp310‑win_amd64.whl
```

### STEP 4: Directory Settings
1. Go to the file /factcode/settingbox.py
There are three directories for the setting, only 'Absolute path' works.
2. Run settingbox.py

### STEP 5: Local Machine Running
1. Setup SDK
```
cloud_sql_proxy.exe -instances="fake-news-base:asia-northeast3:fakenews"=tcp:3306
```
2. Setup Anaconda Prompt, go to environment you made, then go to exact project file
3. Create Table
```
python factcode\model_cloudsql.py
```
4. Run main
```
python main.py
```

### STEP 6: Update Application
```
gcloud app deploy
```


## License
### 1. Team DISFACTCH
For all structure of this project,
    
Copyright 2021 Team Disfactch - Byeongho Hwang, Subin Kim, Yunji Lee, Hanna Jeon

    https://opensource.org/licenses/BSD-3-Clause

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### 2. Google Inc.
For Database connection and html base sturcture,

Copyright 2015 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
    
### 3. 솜씨좋은장씨
For Positivity model,
https://somjang.tistory.com/entry/Keras%EA%B8%B0%EC%82%AC-%EC%A0%9C%EB%AA%A9%EC%9D%84-%EA%B0%80%EC%A7%80%EA%B3%A0-%EA%B8%8D%EC%A0%95-%EB%B6%80%EC%A0%95-%EC%A4%91%EB%A6%BD-%EB%B6%84%EB%A5%98%ED%95%98%EB%8A%94-%EB%AA%A8%EB%8D%B8-%EB%A7%8C%EB%93%A4%EC%96%B4%EB%B3%B4%EA%B8%B0
No license mentioned
