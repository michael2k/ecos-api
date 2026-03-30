"""ECOS API 열거형 정의."""

from enum import StrEnum


class Cycle(StrEnum):
    """통계 주기."""

    ANNUAL = "A"
    QUARTER = "Q"
    QUARTER2 = "QQ"
    MONTHLY = "M"
    MONTHLY2 = "MM"
    SEMI_ANNUAL = "SM"
    DAILY = "D"


class Language(StrEnum):
    """응답 언어."""

    KR = "kr"
    EN = "en"


class ResponseFormat(StrEnum):
    """응답 형식."""

    JSON = "json"
    XML = "xml"
