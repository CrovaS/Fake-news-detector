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
 <img src="" width="">
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
<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131956906-14cb2bc1-8313-4397-b818-5a013474ad57.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>

<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131956983-c0b4be2e-9bbf-43ab-a3eb-1a2a3e296edd.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>

<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131957025-9fe94e04-8d39-4ac9-9156-ae6affad5004.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>

<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131957098-9fddefb4-6fb3-4ff8-b257-ddbe718782de.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>

<p align="center">
    <img src="https://user-images.githubusercontent.com/86072294/131957138-f7e09e03-163e-49d0-9a0c-a22fcfdae4e3.PNG" width="700px">
    <a href="https://github.com/"><img alt="" src=""></a>
</p>

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
positivity_check 부분에 블로그 license 추가 해야할 것 같음.
