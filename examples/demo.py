"""ECOS API 터미널 테스트 스크립트."""

import os
import sys

from ecos import EcosClient, Cycle

API_KEY = os.environ.get("ECOS_API_KEY", "")
if not API_KEY:
    sys.exit("ECOS_API_KEY 환경변수를 설정해주세요. (export ECOS_API_KEY=your_key)")


def main() -> None:
    client = EcosClient(API_KEY)

    print("=" * 70)
    print("1. 주요통계 100선 (상위 10개)")
    print("=" * 70)
    for s in client.get_key_statistics(end_num=10):
        print(f"  {s.class_name:>10} | {s.keystat_name:<25} | {s.data_value} {s.unit_name}")

    print()
    print("=" * 70)
    print("2. 원/달러 환율 (2026.03.01 ~ 2026.03.10, 일별)")
    print("=" * 70)
    for r in client.search("731Y001", Cycle.DAILY, "20260301", "20260310", end_num=10):
        print(f"  {r.time} | {r.item_name1:<25} | {r.data_value} {r.unit_name}")

    print()
    print("=" * 70)
    print("3. 본원통화 (2024.01 ~ 2024.06, 월간)")
    print("=" * 70)
    for r in client.search("102Y004", Cycle.MONTHLY, "202401", "202406", end_num=10):
        print(f"  {r.time} | {r.item_name1:<30} | {r.data_value} {r.unit_name}")

    print()
    print("=" * 70)
    print("4. 통계표 목록 (상위 5개)")
    print("=" * 70)
    for t in client.list_tables(end_num=5):
        print(f"  [{t.stat_code:<12}] {t.stat_name}")

    print()
    print("=" * 70)
    print("5. 통계표 항목 조회 (731Y001 환율)")
    print("=" * 70)
    for item in client.list_items("731Y001", end_num=5):
        print(f"  [{item.item_code}] {item.item_name} ({item.start_time}~{item.end_time})")

    print()
    print("=" * 70)
    print("6. 통계 용어 검색: GDP")
    print("=" * 70)
    for w in client.search_word("GDP"):
        content = w.content.replace("\n", " ")[:80]
        print(f"  {w.word}: {content}...")

    client.close()
    print()
    print("모든 테스트 완료!")


if __name__ == "__main__":
    main()
