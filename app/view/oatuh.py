import mongoengine.errors
import requests
from flask import redirect, request
from flask_classful import FlaskView, route
from flask_apispec import marshal_with, doc
from app.config import Naver, Kakao_2, Google

from app.models.user import User
from app.service.user import UserService
from app.service.auth import *
from app.utils.ApiErrorSchema import *


class OatuhView(FlaskView):
    decorators = (doc(tags=['oauth_login']),)

    @route('/naver')
    @doc(summary="네이버 로그인 URL", description="네이버 로그인요청")
    def naver_login(self):
        url = f"https://nid.naver.com/oauth2.0/authorize?client_id={Naver.client_id}&redirect_uri={Naver.redirect_uri}&response_type=code"
        return redirect(url)

    @route('/naver/callback')
    @doc(summary="네이버 로그인 콜백", description="네이버 로그인 콜백")
    @marshal_with(AuthAllTokenSchema, code=200, description="토큰 발급")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    def naver_callback(self):
        code = request.args["code"]

        token_request = requests.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={Naver.client_id}&client_secret={Naver.client_secret}&code={code}")
        token_json = token_request.json()

        access_token = token_json.get("access_token")
        profile_request = requests.get("https://openapi.naver.com/v1/nid/me",
                                       headers={"Authorization": f"Bearer {access_token}"}, )
        profile_data = profile_request.json()

        social_name = profile_data['response']['name']
        if self.create_user(social_name, 'naver'):
            return UserService.login(social_name, password=None)
        else:
            return NotCreateUsername()

    # @route('/kakao')
    # @doc(summary="카카오 로그인 URL", description="카카오 로그인요청")
    # def kakao_login(self):
    #     url = f"https://kauth.kakao.com/oauth/authorize?client_id={Kakao.client_id}&redirect_uri={Kakao.redirect_uri}&response_type=code"
    #     return redirect(url)

    @route('/kakao/callback')
    @doc(summary="카카오 로그인 콜백", description="카카오 로그인 콜백")
    @marshal_with(ApiErrorSchema, code=409, description="이미 존재하는 사용자")
    @marshal_with(AuthAllTokenSchema, code=200, description="토큰 발급")
    def kakao_callback(self):
        code = request.args["code"]

        # token_request = requests.get(
        #     f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={Kakao.client_id}&client_secret={Kakao.client_secret}&code={code}"
        # )
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={Kakao_2.client_id}&code={code}"
        )
        token_json = token_request.json()

        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_data = profile_request.json()
        social_name = profile_data['properties']['nickname']
        if self.create_user(social_name, 'kakao'):
            return UserService.login(social_name, password=None)
        else:
            return NotCreateUsername()

    @route('/google')
    def google_login(self):
        scope = "https://www.googleapis.com/auth/userinfo.email " + \
                "https://www.googleapis.com/auth/userinfo.profile"
        url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id=${Google.client_id}&redirect_uri=${Google.redirect_uri}&response_type=code&scope={scope}"
        return redirect(url)

    @route('/google/callback')
    def google_callback(self):
        code = request.args["code"]

        token_request = requests.get(
            f"https://accounts.google.com/o/oauth2/v2/token?grant_type=authorization_code&client_id=${Google.client_id}&client_secret=${Google.client_secret}&code={code}"
        )
        token_json = token_request.json()

        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://www.googleapis.com/oauth2/v1/certs",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_data = profile_request.json()
        print(profile_data)

    @classmethod
    def create_user(cls, social_name, provider):
        if not User.objects(username=social_name, provider=provider):
            try:
                user = User(username=social_name, provider=provider)
                user.save()
                return True
            except mongoengine.errors.NotUniqueError:
                return False
        else:
            return True
