

class Config:
    SECRET = '1q2w3e4r1q2w3e4r'
    ALGORITHM = 'HS256'
    TESTING = False
    MONGO_URI = 'mongodb+srv://test:test1234@cluster0.pw9pd.mongodb.net/?retryWrites=true&w=majority'


class TestConfig(Config):
    SECRET = '1q2w3e4r1q2w3e4r'
    ALGORITHM = 'HS256'
    MONGO_URI = 'mongomock://localhost'
    TESTING = True
