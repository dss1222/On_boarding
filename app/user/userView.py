import json
import jwt

from flask_classful import FlaskView, route
from flask import jsonify, request, g, current_app
from bson.json_util import dumps

from app.user.userSchema import UserCreateSchema, UserSchema, UserUpdateSchema
from app.user.userModel import User
from app.utils.validator import user_create_validator, user_validator, login_required
from app.utils.ErrorHandler import *

class UserView(FlaskView):
    #회원가입
    @route('/signup', methods=['POST'])
    @user_create_validator
    def signup(self):

        user = UserCreateSchema().load(json.loads(request.data))

        if user is False:
            return {'message': '이미 등록된 ID입니다.'}, 409

        user.save()
        return Success()

    #로그인
    @route('/login', methods=['POST'])
    @user_validator
    def login(self):
        login_request = json.loads(request.data)
        user = UserSchema().load(login_request)

        if not user:
            return {'message': '존재하지 않는 사용자입니다.'}, 401

        if not user.check_password(login_request['password']):
            return {'message': '잘못된 비밀번호 입니다'}, 401

        token = jwt.encode({"user_id": dumps(user.id), "username": dumps(user.username)},
                           current_app.config['SECRET'], current_app.config['ALGORITHM'])
        print(jwt.decode())
        return jsonify(token), 200

    #회원정보수정
    @route('/update', methods=['PATCH'])
    @login_required
    def update_user(self):
        data = UserUpdateSchema().load(json.loads(request.data))
        user = User.objects(id=g.user_id).get()

        user.update(**data)
        return Success()
