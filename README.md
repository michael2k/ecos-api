# ecos-api

한국은행 경제통계시스템(ECOS) REST API Python 클라이언트

## 설치

```bash
pip install ecos-api
```

## 사용법

[ECOS Open API 인증키](https://ecos.bok.or.kr/)를 발급받아 사용합니다.

### 기본 사용

```python
from ecos import EcosClient, Cycle

client = EcosClient("YOUR_API_KEY")

# 통계 데이터 조회 (GDP, 연간, 2020~2023)
rows = client.search("200Y001", Cycle.ANNUAL, "2020", "2023")
for row in rows:
    print(row.time, row.item_name1, row.data_value)

# 주요통계 100선
stats = client.get_key_statistics()
for s in stats:
    print(s.keystat_name, s.data_value, s.unit_name)

# 통계표 목록 조회
tables = client.list_tables()

# 통계표 항목 조회
items = client.list_items("200Y001")

# 통계표 메타데이터 조회
meta = client.get_meta("200Y001")

# 통계 용어 검색
words = client.search_word("GDP")
```

### 비동기 사용

```python
import asyncio
from ecos import EcosClient, Cycle

async def main():
    async with EcosClient("YOUR_API_KEY") as client:
        rows = await client.search_async("200Y001", Cycle.ANNUAL, "2020", "2023")
        for row in rows:
            print(row.time, row.data_value)

asyncio.run(main())
```

### Context Manager

```python
with EcosClient("YOUR_API_KEY") as client:
    rows = client.search("731Y001", Cycle.DAILY, "20240101", "20240131")
```

## API 메서드

| 메서드 | 비동기 | 설명 |
|--------|--------|------|
| `search()` | `search_async()` | 통계 데이터 조회 |
| `list_tables()` | `list_tables_async()` | 통계표 목록 조회 |
| `list_items()` | `list_items_async()` | 통계 항목 목록 조회 |
| `get_meta()` | `get_meta_async()` | 통계표 메타데이터 조회 |
| `get_key_statistics()` | `get_key_statistics_async()` | 주요통계 100선 |
| `search_word()` | `search_word_async()` | 통계 용어 검색 |

## 주기 코드 (Cycle)

| 값 | 설명 | 날짜 형식 |
|----|------|-----------|
| `Cycle.ANNUAL` | 연간 | `2020` |
| `Cycle.QUARTER` | 분기 | `20201` |
| `Cycle.MONTHLY` | 월간 | `202001` |
| `Cycle.SEMI_ANNUAL` | 반기 | `20201` |
| `Cycle.DAILY` | 일별 | `20200101` |

## 개발

```bash
pip install -e ".[dev]"
pytest
ruff check .
mypy src/
```

## 라이선스

MIT
