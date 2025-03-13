from unittest.mock import patch

from src.clients import SocketSmsClient
from src.http_entities import HttpResponse


@patch("src.clients.SocketClient.request")
def test_socket_sms_client(request_mock, response_bytes) -> None:
    request_mock.return_value = HttpResponse.from_bytes(response_bytes)

    client = SocketSmsClient(
        host="localhost",
        port=4010,
        username="username",
        password="password"
    )
    response = client.send_sms(
        sender="123",
        recipient="456",
        message="abc"
    )

    assert response.to_bytes() == response_bytes
    request_mock.assert_called_with(
        'POST',
        '/send_sms',
        {
            'Authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ=',
        },
        '{"sender": "123", "recipient": "456", "message": "abc"}'
    )
