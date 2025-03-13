from src.http_entities import HttpRequest, HttpResponse


def test_http_request(request_bytes: bytes) -> None:
    rq = HttpRequest.from_bytes(request_bytes)
    assert request_bytes == rq.to_bytes()


def test_http_response(response_bytes: bytes) -> None:
    rp = HttpResponse.from_bytes(response_bytes)
    assert response_bytes == rp.to_bytes()
