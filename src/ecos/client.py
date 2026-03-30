"""ECOS REST API 클라이언트."""

from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ecos.enums import Cycle, Language, ResponseFormat
from ecos.exceptions import EcosAPIError, EcosResponseError
from ecos.models import (
    KeyStatistic,
    StatisticItem,
    StatisticMeta,
    StatisticRow,
    StatisticTable,
    StatisticWord,
)

if TYPE_CHECKING:
    from types import TracebackType

BASE_URL = "https://ecos.bok.or.kr/api"


class EcosClient:
    """한국은행 ECOS Open API 클라이언트.

    Parameters
    ----------
    api_key:
        ECOS Open API 인증키.
    language:
        응답 언어 (기본: 한국어).
    timeout:
        HTTP 요청 타임아웃 (초).

    Examples
    --------
    >>> from ecos import EcosClient, Cycle
    >>> client = EcosClient("YOUR_API_KEY")
    >>> rows = client.search("200Y001", Cycle.ANNUAL, "2020", "2023")
    >>> for row in rows:
    ...     print(row.time, row.data_value)

    비동기 사용:

    >>> async with EcosClient("YOUR_API_KEY") as client:
    ...     rows = await client.search_async("200Y001", Cycle.ANNUAL, "2020", "2023")
    """

    def __init__(
        self,
        api_key: str,
        *,
        language: Language = Language.KR,
        timeout: float = 30.0,
    ) -> None:
        self._api_key = api_key
        self._language = language
        self._sync_client = httpx.Client(base_url=BASE_URL, timeout=timeout)
        self._async_client = httpx.AsyncClient(base_url=BASE_URL, timeout=timeout)

    def close(self) -> None:
        """동기 클라이언트를 닫습니다."""
        self._sync_client.close()

    async def aclose(self) -> None:
        """비동기 클라이언트를 닫습니다."""
        await self._async_client.aclose()

    def __enter__(self) -> EcosClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    async def __aenter__(self) -> EcosClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _build_path(self, service: str, *parts: str | int) -> str:
        segments = [service, self._api_key, self._language, ResponseFormat.JSON, *parts]
        return "/" + "/".join(str(s) for s in segments)

    def _parse_response(self, data: dict, root_key: str) -> list[dict]:
        """API 응답을 파싱하고, 에러가 있으면 예외를 발생시킵니다."""
        if "RESULT" in data:
            result = data["RESULT"]
            raise EcosResponseError(result.get("CODE", ""), result.get("MESSAGE", ""))

        container = data.get(root_key)
        if container is None:
            return []
        return container.get("row", [])

    def _get_sync(self, path: str) -> httpx.Response:
        resp = self._sync_client.get(path)
        if resp.status_code != 200:
            raise EcosAPIError(resp.status_code, resp.text)
        return resp

    async def _get_async(self, path: str) -> httpx.Response:
        resp = await self._async_client.get(path)
        if resp.status_code != 200:
            raise EcosAPIError(resp.status_code, resp.text)
        return resp

    # ------------------------------------------------------------------
    # 통계 데이터 조회 (StatisticSearch)
    # ------------------------------------------------------------------

    def search(
        self,
        stat_code: str,
        cycle: Cycle,
        start_date: str,
        end_date: str,
        *,
        item_code1: str = "?",
        item_code2: str = "?",
        item_code3: str = "?",
        item_code4: str = "?",
        start_num: int = 1,
        end_num: int = 100,
    ) -> list[StatisticRow]:
        """통계 데이터를 조회합니다."""
        path = self._build_path(
            "StatisticSearch",
            start_num,
            end_num,
            stat_code,
            cycle,
            start_date,
            end_date,
            item_code1,
            item_code2,
            item_code3,
            item_code4,
        )
        rows = self._parse_response(self._get_sync(path).json(), "StatisticSearch")
        return [StatisticRow.from_dict(r) for r in rows]

    async def search_async(
        self,
        stat_code: str,
        cycle: Cycle,
        start_date: str,
        end_date: str,
        *,
        item_code1: str = "?",
        item_code2: str = "?",
        item_code3: str = "?",
        item_code4: str = "?",
        start_num: int = 1,
        end_num: int = 100,
    ) -> list[StatisticRow]:
        """통계 데이터를 비동기로 조회합니다."""
        path = self._build_path(
            "StatisticSearch",
            start_num,
            end_num,
            stat_code,
            cycle,
            start_date,
            end_date,
            item_code1,
            item_code2,
            item_code3,
            item_code4,
        )
        resp = await self._get_async(path)
        rows = self._parse_response(resp.json(), "StatisticSearch")
        return [StatisticRow.from_dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 통계표 목록 (StatisticTableList)
    # ------------------------------------------------------------------

    def list_tables(
        self,
        stat_code: str = "",
        *,
        start_num: int = 1,
        end_num: int = 100,
    ) -> list[StatisticTable]:
        """통계표 목록을 조회합니다."""
        path = self._build_path("StatisticTableList", start_num, end_num, stat_code)
        rows = self._parse_response(self._get_sync(path).json(), "StatisticTableList")
        return [StatisticTable.from_dict(r) for r in rows]

    async def list_tables_async(
        self,
        stat_code: str = "",
        *,
        start_num: int = 1,
        end_num: int = 100,
    ) -> list[StatisticTable]:
        """통계표 목록을 비동기로 조회합니다."""
        path = self._build_path("StatisticTableList", start_num, end_num, stat_code)
        resp = await self._get_async(path)
        rows = self._parse_response(resp.json(), "StatisticTableList")
        return [StatisticTable.from_dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 통계 항목 목록 (StatisticItemList)
    # ------------------------------------------------------------------

    def list_items(
        self,
        stat_code: str,
        *,
        start_num: int = 1,
        end_num: int = 100,
    ) -> list[StatisticItem]:
        """특정 통계표의 항목 목록을 조회합니다."""
        path = self._build_path("StatisticItemList", start_num, end_num, stat_code)
        rows = self._parse_response(self._get_sync(path).json(), "StatisticItemList")
        return [StatisticItem.from_dict(r) for r in rows]

    async def list_items_async(
        self,
        stat_code: str,
        *,
        start_num: int = 1,
        end_num: int = 100,
    ) -> list[StatisticItem]:
        """특정 통계표의 항목 목록을 비동기로 조회합니다."""
        path = self._build_path("StatisticItemList", start_num, end_num, stat_code)
        resp = await self._get_async(path)
        rows = self._parse_response(resp.json(), "StatisticItemList")
        return [StatisticItem.from_dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 통계 메타 (StatisticMeta)
    # ------------------------------------------------------------------

    def get_meta(
        self,
        stat_code: str,
        *,
        start_num: int = 1,
        end_num: int = 100,
    ) -> list[StatisticMeta]:
        """통계표 메타데이터를 조회합니다."""
        path = self._build_path("StatisticMeta", start_num, end_num, stat_code)
        rows = self._parse_response(self._get_sync(path).json(), "StatisticMeta")
        return [StatisticMeta.from_dict(r) for r in rows]

    async def get_meta_async(
        self,
        stat_code: str,
        *,
        start_num: int = 1,
        end_num: int = 100,
    ) -> list[StatisticMeta]:
        """통계표 메타데이터를 비동기로 조회합니다."""
        path = self._build_path("StatisticMeta", start_num, end_num, stat_code)
        resp = await self._get_async(path)
        rows = self._parse_response(resp.json(), "StatisticMeta")
        return [StatisticMeta.from_dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 주요통계 100선 (KeyStatisticList)
    # ------------------------------------------------------------------

    def get_key_statistics(
        self,
        *,
        start_num: int = 1,
        end_num: int = 100,
    ) -> list[KeyStatistic]:
        """주요통계 100선을 조회합니다."""
        path = self._build_path("KeyStatisticList", start_num, end_num)
        rows = self._parse_response(self._get_sync(path).json(), "KeyStatisticList")
        return [KeyStatistic.from_dict(r) for r in rows]

    async def get_key_statistics_async(
        self,
        *,
        start_num: int = 1,
        end_num: int = 100,
    ) -> list[KeyStatistic]:
        """주요통계 100선을 비동기로 조회합니다."""
        path = self._build_path("KeyStatisticList", start_num, end_num)
        resp = await self._get_async(path)
        rows = self._parse_response(resp.json(), "KeyStatisticList")
        return [KeyStatistic.from_dict(r) for r in rows]

    # ------------------------------------------------------------------
    # 통계 용어 사전 (StatisticWord)
    # ------------------------------------------------------------------

    def search_word(
        self,
        word: str,
        *,
        start_num: int = 1,
        end_num: int = 20,
    ) -> list[StatisticWord]:
        """통계 용어를 검색합니다."""
        path = self._build_path("StatisticWord", start_num, end_num, word)
        rows = self._parse_response(self._get_sync(path).json(), "StatisticWord")
        return [StatisticWord.from_dict(r) for r in rows]

    async def search_word_async(
        self,
        word: str,
        *,
        start_num: int = 1,
        end_num: int = 20,
    ) -> list[StatisticWord]:
        """통계 용어를 비동기로 검색합니다."""
        path = self._build_path("StatisticWord", start_num, end_num, word)
        resp = await self._get_async(path)
        rows = self._parse_response(resp.json(), "StatisticWord")
        return [StatisticWord.from_dict(r) for r in rows]
