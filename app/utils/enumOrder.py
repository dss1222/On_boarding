import enum


class OrderEnum(enum.Enum):
    created = '-created_at'
    likes = '-likes_cnt'
    comments = '-comments_cnt'
