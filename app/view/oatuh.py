import jwt
import mongoengine.errors
import requests
from flask import Flask, redirect, request, jsonify, g, current_app
from flask_classful import FlaskView, route
from flask_apispec import use_kwargs, marshal_with, doc

from app.models.user import User
from app.service.user import UserService
from app.service.auth import *
from app.utils.ApiErrorSchema import *


class Kakao:
    def __init__(self):
        self.auth_server = "https://kauth.kakao.com%s"
        self.api_server = "https://kapi.kakao.com%s"
        self.default_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }

    def auth(self, code):
        return requests.post(
            url=self.auth_server % "/oauth/token",
            headers=self.default_header,
            data={
                "grant_type": "authorization_code",
                "client_id": 'ed7d28e7036c6bf58342cabf80953f3c',
                "client_secret": 'http://localhost:5000/kakao/logout',
                "redirect_uri": 'http://localhost:5000/kakao/callback',
                "code": code,
            },
        ).json()

    def userinfo(self, bearer_token):
        return requests.post(
            url=self.api_server % "/v2/user/me",
            headers={
                **self.default_header,
                **{"Authorization": bearer_token}
            },
            # "property_keys":'["kakao_account.profile_image_url"]'
            data={}
        ).json()


class OatuhView(FlaskView):
    decorators = (doc(tags=['oauth_login']),)

    @route('/naver')
    @doc(summary="네이버 로그인 URL", description="네이버 로그인요청")
    def naver_login(self):
        client_id = "dbTR7izkNsV7agYg8ODl"
        redirect_uri = "http://localhost:5000/callback"
        # redirect_uri = "http://20.196.249.193:5000/callback"
        url = f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(url)

    @route('/callback')
    @doc(summary="네이버 로그인 콜백", description="네이버 로그인 콜백")
    @marshal_with(AuthAllTokenSchema, code=200, description="토큰 발급")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
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
        if not User.objects(username=social_name, provider='naver'):
            try:
                user = User(username=social_name, provider='naver')
                user.save()
            except mongoengine.errors.NotUniqueError:
                return NotCreateUsername()
        return UserService.login(social_name, password=None)

    @route('/kakao')
    @doc(summary="카카오 로그인 URL", description="카카오 로그인요청")
    def kakao_login(self):
        CLIENT_ID = 'ed7d28e7036c6bf58342cabf80953f3c'
        REDIRECT_URI = 'http://localhost:5000/kakao/callback'
        kakao_oatuh_url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"
        return redirect(kakao_oatuh_url)

    @route('/kakao/callback')
    @doc(summary="카카오 로그인 콜백", description="카카오 로그인 콜백")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @marshal_with(AuthAllTokenSchema, code=200, description="토큰 발급")
    def kakao_callback(self):
        code = request.args["code"]
        # 전달받은 authorization code를 통해서 access_token을 발급
        oauth = Kakao()
        auth_info = oauth.auth(code)

        # error 발생 시 로그인 페이지로 redirect
        if "error" in auth_info:
            print("에러가 발생했습니다.")
            return {'message': '인증 실패'}, 404
        profile_data = oauth.userinfo("Bearer " + auth_info['access_token'])['kakao_account']
        social_name = profile_data['profile']['nickname']
        if not User.objects(username=social_name, provider='kakao'):
            try:
                user = User(username=social_name, provider='kakao')
                user.save()
            except mongoengine.errors.NotUniqueError:
                return NotCreateUsername()

        return UserService.login(social_name, password=None)
