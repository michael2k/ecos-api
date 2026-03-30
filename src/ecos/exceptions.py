"""ECOS API 예외 클래스."""


class EcosError(Exception):
    """ECOS 라이브러리 기본 예외."""


class EcosAPIError(EcosError):
    """ECOS API HTTP 요청 실패."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")


class EcosResponseError(EcosError):
    """ECOS API 응답 에러 (API가 에러 코드를 반환한 경우)."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"[{code}] {message}")
