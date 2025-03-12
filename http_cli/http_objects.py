from typing import Literal, Self

from http_cli.http_abc import AbstractHttp


class Validator:
    headers: dict[str, str]
    body: str | None

    def __init__(self, headers: dict[str, str], body: str | None = None):
        if not isinstance(headers, dict):
            raise TypeError(f"dict expected for headers, got {type(headers)}")
        if body and not isinstance(body, str):
            raise TypeError(f"str expected for body, got {type(body)}")

        for k, v in headers.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError(
                    "dict[str, str] expected for headers, got other types of keys or values"
                )

        self.headers = headers
        self.body = body


class HttpRequest(AbstractHttp, Validator):
    method: Literal[
        "GET", "POST"
    ]  # только POST требуется в задаче, поэтому не весь список
    path: str

    __slots__ = ("method", "path", "headers", "body")

    def __init__(
        self,
        method: Literal["GET", "POST"],
        path: str,
        headers: dict[str, str],
        body: str | None,
    ):
        # без проверки для метода, поскольку подсказка в виде литерала
        if not isinstance(path, str):
            raise TypeError(f"str expected for path, got {type(path)}")

        super().__init__(headers, body)

        if "Host" not in headers.keys():
            raise ValueError("Host header is required")

        if body and "Content-Length" not in headers.keys():
            headers.update({"Content-Length": str(len(body))})

        self.method = method
        self.path = path

    def __str__(self):
        headers = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])
        request_str = (
            f"{self.method} {self.path} HTTP/1.1\r\n"
            f"{headers}\r\n\r\n"
            f"{self.body if self.body else ''}"
        )
        return request_str

    def to_bytes(self) -> bytes:
        return str(self).encode("utf-8")

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        request_str = binary_data.decode("utf-8")
        parts = request_str.split("\r\n\r\n", 1)
        header_part = parts[0]
        body = parts[1] if len(parts) > 1 else None

        lines = header_part.split("\r\n")
        start_line = lines[0]
        headers = {}

        method, path, _ = start_line.split(" ", 2)
        for line in lines[1:]:
            if line:
                k, v = line.split(": ", 1)
                headers.update({k: v})

        return cls(method, path, headers, body)


class HttpResponse(AbstractHttp, Validator):
    status_code: int

    __slots__ = ("status_code", "headers", "body")

    def __init__(self, status_code: int, headers: dict[str, str], body: str | None):
        if not isinstance(status_code, int):
            raise TypeError(f"int expected for status_code, got {type(status_code)}")

        super().__init__(headers, body)

        self.status_code = status_code

    def __str__(self):
        status_line = f"HTTP/1.1 {self.status_code}\r\n"
        headers = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])
        response_str = f"{status_line}" f"{headers}\r\n\r\n" f"{self.body}"
        return response_str

    def to_bytes(self) -> bytes:
        return str(self).encode("utf-8")

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        response_str = binary_data.decode("utf-8")
        parts = response_str.split("\r\n\r\n", 1)
        header_part = parts[0]
        body = parts[1] if len(parts) > 1 else ""

        lines = header_part.split("\r\n")
        status_line = lines[0]
        status_code = status_line.split(" ", 2)[1]
        headers = {}
        for line in lines[1:]:
            if line:
                k, v = line.split(": ", 1)
                headers.update({k: v})

        return cls(int(status_code), headers, body)
