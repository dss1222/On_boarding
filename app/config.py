from app.practice_secret import *


class Config:
    SECRET = '1q2w3e4r1q2w3e4r'
    ALGORITHM = 'HS256'
    TESTING = False
    MONGO_URI = 'mongodb://localhost:27017/practice'


class TestConfig(Config):
    SECRET = '1q2w3e4r1q2w3e4r'
    ALGORITHM = 'HS256'
    MONGO_URI = 'mongomock://localhost'
    TESTING = True


# 만약 aws계정관련 config가 추가되어야 한다면 따로 파일을 하나 더만들고
# 하나 더 만든 파일에 계정정보담아둔다 이 config에선 해당 계정정보를 변수로 가져온다
# 그리고 github에 커밋 할때 이 config.py는 업로드하지만 따로 만든 파일은 업로드하지 않음

# 이유 : aws계정관련을 깃에 올리면 악의를 가진 누군가가 도용할 수 있음
# 연습이기에 pratice_secret도 같이 커밋함
print(secret_key)
print(aws_id)
