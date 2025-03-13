import pytest


@pytest.fixture
def request_bytes() -> bytes:
    s = ('POST /send_sms HTTP/1.1\r\n'
         'Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=\r\n'
         'Host: localhost\r\n'
         'Content-Type: application/json\r\n'
         'Content-Length: 55\r\n\r\n'
         '{"sender": "123", "recipient": "456", "message": "abc"}')
    return s.encode('utf-8')


@pytest.fixture
def response_bytes() -> bytes:
    s = ('HTTP/1.1 200 OK\r\n'
         'Access-Control-Allow-Origin: *\r\n'
         'Access-Control-Allow-Headers: *\r\n'
         'Access-Control-Allow-Credentials: true\r\n'
         'Access-Control-Expose-Headers: *\r\n'
         'Content-type: application/json\r\n'
         'Content-Length: 42\r\n'
         'Date: Tue, 12 Mar 2025 19:14:11 GMT\r\n'
         'Connection: keep-alive\r\n'
         'Keep-Alive: timeout=5\r\n\r\n'
         '{"status":"success","message_id":"123456"}')
    return s.encode('utf-8')
