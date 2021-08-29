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
import pickle
from keras.models import load_model
# import numpy as np

def get_data_directory(traincsv_directory, testcsv_directory):

    train_data = pd.read_csv(traincsv_directory)
    test_data = pd.read_csv(testcsv_directory)

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
    X_train = []
    for sentence in train_data['title']:
        temp_X = []
        temp_X = okt.morphs(sentence, stem=True) # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
        X_train.append(temp_X)

    X_test = []
    for sentence in test_data['title']:
        temp_X = []
        temp_X = okt.morphs(sentence, stem=True) # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
        X_test.append(temp_X)

    max_words = 35000
    tokenizer = Tokenizer(num_words = max_words)
    tokenizer.fit_on_texts(X_train)
    X_train = tokenizer.texts_to_sequences(X_train)
    X_test = tokenizer.texts_to_sequences(X_test)

    return train_data, test_data, X_train, X_test, tokenizer

def make_positivity_model(train_data, test_data, X_train, X_test):
    import numpy as np
    y_train = []
    y_test = []

    for i in range(len(train_data['label'])):
        if train_data['label'].iloc[i] == 1:
            y_train.append([0, 0, 1])
        elif train_data['label'].iloc[i] == 0:
            y_train.append([0, 1, 0])
        elif train_data['label'].iloc[i] == -1:
            y_train.append([1, 0, 0])

    for i in range(len(test_data['label'])):
        if test_data['label'].iloc[i] == 1:
            y_test.append([0, 0, 1])
        elif test_data['label'].iloc[i] == 0:
            y_test.append([0, 1, 0])
        elif test_data['label'].iloc[i] == -1:
            y_test.append([1, 0, 0])

    y_train = np.array(y_train)
    y_test = np.array(y_test)

    from keras.layers import Embedding, Dense, LSTM
    from keras.models import Sequential
    from keras.preprocessing.sequence import pad_sequences
    max_len = 20 # 전체 데이터의 길이를 20로 맞춘다
    max_words = 35000

    X_train = pad_sequences(X_train, maxlen=max_len)
    X_test = pad_sequences(X_test, maxlen=max_len)

    model = Sequential()
    model.add(Embedding(max_words, 100))
    model.add(LSTM(128))
    model.add(Dense(3, activation='softmax'))
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(X_train, y_train, epochs=10, batch_size=10, validation_split=0.1)

    print("\n 테스트 정확도 : {:.2f}".format(model.evaluate(X_test, y_test)[1]*100))

    return model

def train_positivity_model(traincsv_directory, testcsv_directory):
    
    train_data, test_data, X_train, X_test, tokenizer = get_data_directory(traincsv_directory, testcsv_directory)
    model = make_positivity_model(train_data, test_data, X_train, X_test)

    try:
        with open('positivitymodel.p', 'wb') as file:    # positivitymodel.p 파일을 바이너리 쓰기 모드(wb)로 열기
            pickle.dump(tokenizer, file)

        model.save('mnist_mlp_model.h5')
        
        return 1
    except: return 0

def positivity_train_main(train_directory, test_directory):

    ok_or_not = train_positivity_model(train_directory, test_directory)
    if ok_or_not == 1: print("Wow! Model is perfectly saved!")
    elif ok_or_not == 0: print("Oh, no... There is a error in the model.")
    else: print("Error in something else.")
    return 0


if __name__ == '__main__':
    traincsv_directory = ".../train_dataset_1007.csv"
    testcsv_directory = ".../test_dataset_1007.csv"

    ok_or_not = train_positivity_model(traincsv_directory, testcsv_directory)
    if ok_or_not == 1: print("Wow! Model is perfectly saved!")
    elif ok_or_not == 0: print("Oh, no... There is a error in the model.")
    else: print("Error in something else.")