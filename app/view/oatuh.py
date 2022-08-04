import jwt
import requests
from flask import Flask, redirect, request, jsonify, g, current_app
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc

from app.models.user import User
from app.service.user import UserService
from app.service.auth import *


class OatuhView(FlaskView):
    decorators = (doc(tags=['Naver_Login']),)

    @route('/naver')
    @doc(summary="로그인 URL", description="네이버 로그인요청")
    def naver_login(self):
        client_id = "dbTR7izkNsV7agYg8ODl"
        redirect_uri = "http://localhost:5000/callback"
        # redirect_uri = "http://20.196.249.193:5000/callback"
        url = f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(url)

    @route('/callback')
    @doc(summary="로그인 콜백", description="네이버 콜백")
    @marshal_with(AuthAllTokenSchema, code=200, description="토큰 발급")
    def naver_callback(self):
        params = request.args.to_dict()
        code = params.get("code")

        client_id = "dbTR7izkNsV7agYg8ODl"
        client_secret = "76chnohmXX"
        # redirect_uri = "http://localhost:5000/callback"
        redirect_uri = "http://20.196.249.193:5000/callback"

        token_request = requests.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}")
        token_json = token_request.json()

        access_token = token_json.get("access_token")
        profile_request = requests.get("https://openapi.naver.com/v1/nid/me",
                                       headers={"Authorization": f"Bearer {access_token}"}, )
        profile_data = profile_request.json()

        social_name = profile_data['response']['name']
        if not User.objects(username=social_name):
            user = User(username=social_name, provider='naver')
            user.save()

        return UserService.login(social_name, password=None)
