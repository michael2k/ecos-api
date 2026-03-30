"""빌드 스크립트 — 패치 버전을 자동 증가시키고 빌드를 실행합니다."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"
INIT = ROOT / "src" / "ecos" / "__init__.py"


def bump_patch(version: str) -> str:
    major, minor, patch = version.split(".")
    return f"{major}.{minor}.{int(patch) + 1}"


def update_file(path: Path, pattern: str, new_version: str) -> None:
    text = path.read_text()
    updated = re.sub(pattern, lambda m: m.group(0).replace(m.group(1), new_version), text)
    path.write_text(updated)


def main() -> None:
    # 현재 버전 읽기
    text = PYPROJECT.read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        sys.exit("pyproject.toml에서 version을 찾을 수 없습니다.")

    old = match.group(1)
    new = bump_patch(old)

    # pyproject.toml + __init__.py 버전 갱신
    update_file(PYPROJECT, r'version\s*=\s*"([^"]+)"', new)
    update_file(INIT, r'__version__\s*=\s*"([^"]+)"', new)

    print(f"버전: {old} → {new}")

    # 빌드
    result = subprocess.run([sys.executable, "-m", "build"], cwd=ROOT)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
