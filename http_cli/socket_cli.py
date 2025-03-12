import base64
import json
import socket
from typing import Literal

from http_cli.http_objects import HttpRequest, HttpResponse


class SocketClient:
    host: str
    port: int

    def __init__(self, host: str, port: int):
        if not isinstance(host, str):
            raise TypeError(f'str expected for host, got {type(host)}')
        if not isinstance(port, int):
            raise TypeError(f'int expected for port, got {type(port)}')

        self.host = host
        self.port = port

    def request(self, method: Literal["GET", "POST"],
                 path: str, headers: dict[str, str], body: str | None) -> HttpResponse:
        if not isinstance(headers, dict):
            raise TypeError(f'dict expected for headers, got {type(headers)}')

        headers.update({
            "Host": self.host,
            "Content-Type": "application/json"
        })

        rq = HttpRequest(method, path, headers, body)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(rq.to_bytes())

            response = s.recv(4096)
            return HttpResponse.from_bytes(response)

    def post(self, path: str, headers: dict[str, str], body: str | None) -> HttpResponse:
        return self.request('POST', path, headers, body)


class BasicAuthSocketClient(SocketClient):
    __auth_header: str

    def __init__(self, host: str, port: int,
                 username: str, password: str):
        if not isinstance(username, str):
            raise TypeError(f'str expected for username, got {type(username)}')
        if not isinstance(password, str):
            raise TypeError(f'str expected for password, got {type(password)}')

        super().__init__(host, port)

        self.__auth_header = base64.b64encode(f"{username}:{password}".encode()).decode()

    def request(self, method: Literal["GET", "POST"],
                 path: str, headers: dict[str, str], body: str | None) -> HttpResponse:
        if not isinstance(headers, dict):
            raise TypeError(f'dict expected for headers, got {type(headers)}')

        headers.update({'Authorization': f'Basic {self.__auth_header}'})
        return super().request(method, path, headers, body)

    def post(self, path: str, headers: dict[str, str], body: str | None):
        return self.request('POST', path, headers, body)


class SocketSmsClient(BasicAuthSocketClient):
    def __init__(self, host: str, port: int,
                 username: str, password: str):
        super().__init__(host, port, username, password)

    def send_sms(self, sender: str, recipient: str, message: str) -> HttpResponse:
        if not isinstance(sender, str):
            raise TypeError(f'str expected for sender, got {type(sender)}')
        if not isinstance(recipient, str):
            raise TypeError(f'str expected for recipient, got {type(recipient)}')
        if not isinstance(message, str):
            raise TypeError(f'str expected for message, got {type(message)}')

        body = json.dumps({
            "sender": sender,
            "recipient": recipient,
            "message": message
        })

        # необходимые заголовки формируются на внутренних слоях
        return self.post('/send_sms', dict(), body)
