from app.secret_config import MongoAtlas


class Config:
    SECRET = '1q2w3e4r1q2w3e4r'
    ALGORITHM = 'HS256'
    TESTING = False
    # MONGO_URI = 'mongodb+srv://' + MongoAtlas.secret_id + ':' + MongoAtlas.secret_password + '@cluster0.pw9pd.mongodb.net/?retryWrites=true&w=majority'
    MONGO_URI = 'mongodb://localhost:27017/practice'
    # MONGO_URI = 'mongodb+srv://1q2w3e4r:1q2w3e4r@cluster0.pw9pd.mongodb.net/?retryWrites=true&w=majority'


class TestConfig(Config):
    SECRET = '1q2w3e4r1q2w3e4r'
    ALGORITHM = 'HS256'
    MONGO_URI = 'mongomock://localhost'
    TESTING = True


class Naver:
    client_id = "dbTR7izkNsV7agYg8ODl"
    client_secret = "76chnohmXX"
    # redirect_uri = "http://localhost:5000/callback"
    redirect_uri = "http://20.196.249.193:5000/naver/callback"  # 배포


class Kakao:
    client_id = 'ed7d28e7036c6bf58342cabf80953f3c'
    client_secret = 'TIfBV2wic46YaZnTJ0PbJNwD5yap3IYT'
    # redirect_uri = 'http://localhost:5000/kakao/callback'
    redirect_uri = 'http://20.196.249.193:5000//kakao/callback'  # 배포


class Google:
    client_id = '359760661847-64femk3is6luubq7cb03kntejqr4glbf.apps.googleusercontent.com'
    client_secret = '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'
    # redirect_uri = 'http://localhost:5000/google/callback'
    redirect_uri = 'http://20.196.249.193:5000/google/callback'  # 배포
