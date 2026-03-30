"""EcosClient 테스트."""

import httpx
import pytest
import respx

from ecos import Cycle, EcosClient, EcosResponseError


API_KEY = "test-key"
BASE = "https://ecos.bok.or.kr/api"


@pytest.fixture
def client():
    with EcosClient(API_KEY) as c:
        yield c


class TestSearch:
    @respx.mock
    def test_search_returns_rows(self, client: EcosClient):
        url = f"{BASE}/StatisticSearch/{API_KEY}/kr/json/1/100/200Y001/A/2020/2023/?/?/?/?"
        respx.get(url).respond(
            json={
                "StatisticSearch": {
                    "list_total_count": 1,
                    "row": [
                        {
                            "STAT_CODE": "200Y001",
                            "STAT_NAME": "GDP",
                            "ITEM_CODE1": "10101",
                            "ITEM_NAME1": "국내총생산(GDP)",
                            "ITEM_CODE2": "",
                            "ITEM_NAME2": "",
                            "ITEM_CODE3": "",
                            "ITEM_NAME3": "",
                            "ITEM_CODE4": "",
                            "ITEM_NAME4": "",
                            "UNIT_NAME": "십억원",
                            "WGT": "",
                            "TIME": "2020",
                            "DATA_VALUE": "1933",
                        }
                    ],
                }
            }
        )

        rows = client.search("200Y001", Cycle.ANNUAL, "2020", "2023")
        assert len(rows) == 1
        assert rows[0].stat_code == "200Y001"
        assert rows[0].data_value == "1933"

    @respx.mock
    def test_search_api_error_raises(self, client: EcosClient):
        url = f"{BASE}/StatisticSearch/{API_KEY}/kr/json/1/100/INVALID/A/2020/2023/?/?/?/?"
        respx.get(url).respond(
            json={"RESULT": {"CODE": "ERROR", "MESSAGE": "Invalid stat code"}}
        )

        with pytest.raises(EcosResponseError, match="Invalid stat code"):
            client.search("INVALID", Cycle.ANNUAL, "2020", "2023")


class TestListTables:
    @respx.mock
    def test_list_tables(self, client: EcosClient):
        url = f"{BASE}/StatisticTableList/{API_KEY}/kr/json/1/100/"
        respx.get(url).respond(
            json={
                "StatisticTableList": {
                    "list_total_count": 1,
                    "row": [
                        {
                            "STAT_CODE": "200Y001",
                            "STAT_NAME": "주요지표",
                            "GRP_CODE": "GRP1",
                            "GRP_NAME": "그룹",
                            "ORG_NAME": "한국은행",
                            "CYCLE": "A",
                        }
                    ],
                }
            }
        )

        tables = client.list_tables()
        assert len(tables) == 1
        assert tables[0].stat_code == "200Y001"


class TestKeyStatistics:
    @respx.mock
    def test_get_key_statistics(self, client: EcosClient):
        url = f"{BASE}/KeyStatisticList/{API_KEY}/kr/json/1/100"
        respx.get(url).respond(
            json={
                "KeyStatisticList": {
                    "list_total_count": 1,
                    "row": [
                        {
                            "CLASS_NAME": "금리",
                            "KEYSTAT_NAME": "한국은행 기준금리",
                            "DATA_VALUE": "3.50",
                            "CYCLE": "D",
                            "UNIT_NAME": "% 연",
                            "TIME": "20240101",
                        }
                    ],
                }
            }
        )

        stats = client.get_key_statistics()
        assert len(stats) == 1
        assert stats[0].keystat_name == "한국은행 기준금리"


class TestSearchAsync:
    @respx.mock
    @pytest.mark.asyncio
    async def test_search_async(self):
        url = f"{BASE}/StatisticSearch/{API_KEY}/kr/json/1/100/200Y001/A/2020/2023/?/?/?/?"
        respx.get(url).respond(
            json={
                "StatisticSearch": {
                    "list_total_count": 1,
                    "row": [
                        {
                            "STAT_CODE": "200Y001",
                            "STAT_NAME": "GDP",
                            "ITEM_CODE1": "10101",
                            "ITEM_NAME1": "국내총생산(GDP)",
                            "ITEM_CODE2": "",
                            "ITEM_NAME2": "",
                            "ITEM_CODE3": "",
                            "ITEM_NAME3": "",
                            "ITEM_CODE4": "",
                            "ITEM_NAME4": "",
                            "UNIT_NAME": "십억원",
                            "WGT": "",
                            "TIME": "2020",
                            "DATA_VALUE": "1933",
                        }
                    ],
                }
            }
        )

        async with EcosClient(API_KEY) as client:
            rows = await client.search_async("200Y001", Cycle.ANNUAL, "2020", "2023")
            assert len(rows) == 1
            assert rows[0].data_value == "1933"
