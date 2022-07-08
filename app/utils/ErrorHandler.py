import json
from flask import jsonify


def Success():
    return jsonify("성공"), 200


def NotLoginUser():
    return jsonify("로그인하지 않은 사용자입니다"), 401


def NotInvalidToken():
    return jsonify("유효하지 않은 토큰입니다"), 401


def NotCreatedUser():
    return jsonify("게시글 작성자가 아닙니다"), 403


def NotFoundPost():
    return jsonify("해당 게시글이 존재하지 않습니다."), 404


def NotFoundComment():
    return jsonify("해당 댓글이 존재하지 않습니다"), 404


def NotFoundBoard():
    return jsonify("해당 게시판이 존재하지 않습니다"), 404


def WrongId():
    return jsonify("잘못된 id 형식입니다"), 404


def CreatedError():
    return jsonify("잘못된 요청입니다"), 422
