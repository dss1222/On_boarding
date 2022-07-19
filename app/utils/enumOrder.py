from enum import Enum


class OrderEnum(Enum):
    created = '-created_at'
    likes = '-likes_cnt'
    comments = '-comments_cnt'
