"""ECOS API 응답 모델."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class StatisticRow:
    """통계 데이터 행."""

    stat_code: str
    stat_name: str
    item_code1: str
    item_name1: str
    item_code2: str
    item_name2: str
    item_code3: str
    item_name3: str
    item_code4: str
    item_name4: str
    unit_name: str
    wgt: str
    time: str
    data_value: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StatisticRow:
        return cls(
            stat_code=data.get("STAT_CODE", ""),
            stat_name=data.get("STAT_NAME", ""),
            item_code1=data.get("ITEM_CODE1", ""),
            item_name1=data.get("ITEM_NAME1", ""),
            item_code2=data.get("ITEM_CODE2", ""),
            item_name2=data.get("ITEM_NAME2", ""),
            item_code3=data.get("ITEM_CODE3", ""),
            item_name3=data.get("ITEM_NAME3", ""),
            item_code4=data.get("ITEM_CODE4", ""),
            item_name4=data.get("ITEM_NAME4", ""),
            unit_name=data.get("UNIT_NAME", ""),
            wgt=data.get("WGT", ""),
            time=data.get("TIME", ""),
            data_value=data.get("DATA_VALUE", ""),
        )


@dataclass(frozen=True, slots=True)
class StatisticTable:
    """통계표 정보."""

    stat_code: str
    stat_name: str
    grp_code: str
    grp_name: str
    org_name: str
    cycle: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StatisticTable:
        return cls(
            stat_code=data.get("STAT_CODE", ""),
            stat_name=data.get("STAT_NAME", ""),
            grp_code=data.get("GRP_CODE", ""),
            grp_name=data.get("GRP_NAME", ""),
            org_name=data.get("ORG_NAME", ""),
            cycle=data.get("CYCLE", ""),
        )


@dataclass(frozen=True, slots=True)
class StatisticItem:
    """통계표 항목."""

    stat_code: str
    stat_name: str
    grp_code: str
    grp_name: str
    item_code: str
    item_name: str
    cycle: str
    start_time: str
    end_time: str
    data_cnt: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StatisticItem:
        return cls(
            stat_code=data.get("STAT_CODE", ""),
            stat_name=data.get("STAT_NAME", ""),
            grp_code=data.get("GRP_CODE", ""),
            grp_name=data.get("GRP_NAME", ""),
            item_code=data.get("ITEM_CODE", ""),
            item_name=data.get("ITEM_NAME", ""),
            cycle=data.get("CYCLE", ""),
            start_time=data.get("START_TIME", ""),
            end_time=data.get("END_TIME", ""),
            data_cnt=data.get("DATA_CNT", ""),
        )


@dataclass(frozen=True, slots=True)
class StatisticMeta:
    """통계표 메타데이터."""

    stat_code: str
    stat_name: str
    stat_memo: str
    org_name: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StatisticMeta:
        return cls(
            stat_code=data.get("STAT_CODE", ""),
            stat_name=data.get("STAT_NAME", ""),
            stat_memo=data.get("STAT_MEMO", ""),
            org_name=data.get("ORG_NAME", ""),
        )


@dataclass(frozen=True, slots=True)
class KeyStatistic:
    """주요통계 100선."""

    class_name: str
    keystat_name: str
    data_value: str
    cycle: str
    unit_name: str
    time: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> KeyStatistic:
        return cls(
            class_name=data.get("CLASS_NAME", ""),
            keystat_name=data.get("KEYSTAT_NAME", ""),
            data_value=data.get("DATA_VALUE", ""),
            cycle=data.get("CYCLE", ""),
            unit_name=data.get("UNIT_NAME", ""),
            time=data.get("TIME", ""),
        )


@dataclass(frozen=True, slots=True)
class StatisticWord:
    """통계 용어."""

    word: str
    content: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StatisticWord:
        return cls(
            word=data.get("WORD", ""),
            content=data.get("CONTENT", ""),
        )
