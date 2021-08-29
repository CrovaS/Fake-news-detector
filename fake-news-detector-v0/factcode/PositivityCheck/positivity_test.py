# positivity_test.py

# Original by 솜시좋은장씨
# Editted by Hanna Jeon (전한나), Byeongho Hwang (황병호)

# positivity_test.py는 긍정/부정 정도 판별 모델을 직접 이용하는 모듈을 모아놓은 파일이다.

# Licensed by
# https://somjang.tistory.com/entry/Keras%EA%B8%B0%EC%82%AC-%EC%A0%9C%EB%AA%A9%EC%9D%84-%EA%B0%80%EC%A7%80%EA%B3%A0-%EA%B8%8D%EC%A0%95-%EB%B6%80%EC%A0%95-%EC%A4%91%EB%A6%BD-%EB%B6%84%EB%A5%98%ED%95%98%EB%8A%94-%EB%AA%A8%EB%8D%B8-%EB%A7%8C%EB%93%A4%EC%96%B4%EB%B3%B4%EA%B8%B0


from re import X
from keras_preprocessing.text import tokenizer_from_json
import pandas as pd
from keras.preprocessing.text import Tokenizer
# import numpy as np

def get_titleset(tokenizer, title):

    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

    # Import JPype for Konlpy
    try:
        import jpype
        import jpype1
    except:
        import jpype

    import konlpy
    from konlpy.tag import Okt

    okt = Okt()

    title_list = []
    temp_X = []
    temp_X = okt.morphs(title, stem=True) # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    title_list.append(temp_X)

    title_list = tokenizer.texts_to_sequences(title_list)

    return title_list

def prediction(model, titleset):
    import numpy as np
    
    predict_res = model.predict(titleset)
    label = np.argmax(predict_res, axis=1)
    result = label[0]

    return result

def use_positivity_model(title):
    import pickle
    from keras.models import load_model
 
    with open('positivitymodel.p', 'rb') as file:    # positivitymodel.p 파일을 바이너리 읽기 모드(rb)로 열기
        tokenizer = pickle.load(file)
    
    model = load_model('mnist_mlp_model.h5')
    
    titleset = get_titleset(tokenizer, title)
    positivity = prediction(model, titleset)
    positivity = positivity - 1

    return positivity


if __name__ == '__main__':
    # title = '더벨맘스터치 가맹점포 롯데리아 앞질러1위 우뚝'
    title = '롯데리아도 맘스터치도 패스트푸드점 위생적발 5년간 50 증가'
    # title = '맘스터치 도시락 한 달만에 3만개 완판잘 나가는 치킨 프랜차이즈 간편식'
    # title = '맘스터치 먹고 뉴이스트 · 옹성우 · 여자친구 보러가자'
    # title = 'MTM터치 연중기획공연12세계의 음악도시 오스틴 내슈빌 아바나'

    positivity = use_positivity_model(title)
    print(positivity)