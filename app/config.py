from app.secret_config import MongoAtlas


class Config:
    SECRET = '1q2w3e4r1q2w3e4r'
    ALGORITHM = 'HS256'
    TESTING = False
    MONGO_URI = 'mongodb+srv://' + MongoAtlas.secret_id + ':' + MongoAtlas.secret_password + '@cluster0.pw9pd.mongodb.net/?retryWrites=true&w=majority'
    # MONGO_URI = 'mongodb://localhost:27017/practice'
    # MONGO_URI = 'mongodb+srv://1q2w3e4r:1q2w3e4r@cluster0.pw9pd.mongodb.net/?retryWrites=true&w=majority'

class TestConfig(Config):
    SECRET = '1q2w3e4r1q2w3e4r'
    ALGORITHM = 'HS256'
    MONGO_URI = 'mongomock://localhost'
    TESTING = True
