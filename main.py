import json

from http_cli.socket_cli import SocketSmsClient

if __name__ == '__main__':
    client = SocketSmsClient(
        host='localhost',
        port=4010,
        username='username',
        password='password'
    )
    try:
        response = client.send_sms(
            sender='88005553535',
            recipient='89997895634',
            message='Ну что там с деньгами?'
        )
        print(f'Код ответа: {response.status_code}')
        print('Тело ответа:')
        print(json.dumps(json.loads(response.body), indent=4))
    except ConnectionError as e:
        print(f'Не удалось установить подключение:\n{e}')
