

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
