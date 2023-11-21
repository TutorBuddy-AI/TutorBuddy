from . import BaseEnum


class DailyNewsEnum(BaseEnum):
    NEWS_TYPE__TEXT = 'text'
    NEWS_TYPE__IMAGE = 'image'
    NEWS_TYPE__FILE = 'file'
    NEWS_TYPE__VIDEO = 'video'
