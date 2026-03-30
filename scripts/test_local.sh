#!/bin/bash
# 로컬 프로젝트 소스로 단위 테스트 + 실제 API 테스트를 실행하는 스크립트

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$SCRIPT_DIR/.."
ENV_FILE="$ROOT/.env"

# .env 파일에서 API 키 로드
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

if [ -z "$ECOS_API_KEY" ]; then
    echo "ECOS_API_KEY 환경변수를 설정해주세요."
    exit 1
fi

echo "=========================================="
echo " 0. 의존성 설치"
echo "=========================================="
pip install -q -e "$ROOT[dev]"

echo ""
echo "=========================================="
echo " 1. 단위 테스트 (mock)"
echo "=========================================="
python -m pytest "$ROOT/tests" -v

echo ""
echo "=========================================="
echo " 2. 실제 API 테스트"
echo "=========================================="
ECOS_API_KEY="$ECOS_API_KEY" python "$ROOT/examples/demo.py"
