# settingbox.py
# Written by Byeongho Hwang (황병호)

# settingbox.py는 일일이 찾아가 수정하기 어려운 디렉토리를 단번에 수정할 수 있도록
# 제작한 디렉토리 저장용 / 실제 사용전 인공지능 모델 트레이닝용 파일이다.

# SPDX-FileCopyrightText: © 2021 Byeongho Hwang <crovas@kaist.ac.kr>
# SPDX-License-Identifier: BSD-3-Clause


def get_directory(what_you_want):
    directory = ''
    # Type '.../factChecker/factcode/PositivityCheck/train_dataset_1007.csv' in your disk
    if what_you_want == 'train_directory':
        directory = "C:/Ekenda Bia/Fact Checker/factChecker/factcode/PositivityCheck/train_dataset_1007.csv"
    # Type '.../factChecker/factcode/PositivityCheck/test_dataset_1007.csv' in your disk
    if what_you_want == 'test_directory':
        directory = "C:/Ekenda Bia/Fact Checker/factChecker/factcode/PositivityCheck/test_dataset_1007.csv"
    # Type '.../factChecker/selenium/chromedriver.exe' in your disk
    if what_you_want == 'chromedriver':
        directory = "C:/Ekenda Bia/Fact Checker/factChecker/selenium/chromedriver.exe"
    
    return directory

def train_positivity_model():
    try:
        from PositivityCheck import positivity_train
        pt = positivity_train
        train_directory = get_directory('train_directory')
        test_directory = get_directory('test_directory')
        pt.positivity_train_main(train_directory, test_directory)
        message = 'DONE!'
    except:
        message = 'ERROR...'
    return message

if __name__ == '__main__':
    result = train_positivity_model()
    print(result)