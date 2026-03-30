#!/bin/bash
# PyPI에 배포된 ecos-api 패키지를 설치하고 테스트하는 스크립트

set -e

# .env 파일에서 API 키 로드
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

if [ -z "$ECOS_API_KEY" ]; then
    echo "ECOS_API_KEY 환경변수를 설정해주세요."
    echo "  export ECOS_API_KEY=your_key"
    exit 1
fi

# 임시 가상환경 생성
TMPDIR=$(mktemp -d)
echo "임시 환경: $TMPDIR"
python -m venv "$TMPDIR/venv"
source "$TMPDIR/venv/bin/activate"

echo ""
echo "=========================================="
echo " 1. PyPI에서 ecos-api 설치"
echo "=========================================="
pip install --quiet ecos-api
echo "  설치 완료: $(pip show ecos-api | grep Version)"

echo ""
echo "=========================================="
echo " 2. API 테스트 실행"
echo "=========================================="
python -c "
from ecos import EcosClient, Cycle, __version__
import os

key = os.environ['ECOS_API_KEY']
client = EcosClient(key)

print(f'  ecos-api v{__version__}')
print()

# 주요통계 100선
print('  [주요통계 100선]')
for s in client.get_key_statistics(end_num=5):
    print(f'    {s.class_name:>8} | {s.keystat_name:<20} | {s.data_value} {s.unit_name}')

print()

# 환율 조회
print('  [원/달러 환율 - 최근 5건]')
for r in client.search('731Y001', Cycle.DAILY, '20260301', '20260330',
                        item_code1='0000001', end_num=5):
    print(f'    {r.time} | {r.data_value} {r.unit_name}')

print()

# 통계표 목록
print('  [통계표 목록 - 상위 3개]')
for t in client.list_tables(end_num=3):
    print(f'    [{t.stat_code}] {t.stat_name}')

print()

# 통계 항목
print('  [731Y001 환율 항목 - 상위 3개]')
for item in client.list_items('731Y001', end_num=3):
    print(f'    [{item.item_code}] {item.item_name}')

print()

# 용어 검색
print('  [용어 검색: 환율]')
for w in client.search_word('환율'):
    content = w.content.replace(chr(10), ' ')[:60]
    print(f'    {w.word}: {content}...')

client.close()
print()
print('  모든 API 테스트 통과!')
"

# 정리
deactivate
rm -rf "$TMPDIR"
echo ""
echo "임시 환경 정리 완료."
