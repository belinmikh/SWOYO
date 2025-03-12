import logging
import sys
import tomllib

from http_cli.socket_cli import SocketSmsClient

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(
            "Недопустимое выполнение! Формат запуска:\n"
            "python main.py номер_отправителя номер_получателя 'текст сообщения'"
        )

    sender, recipient, message = sys.argv[1:]

    try:
        with open("conf.toml", "rb") as toml:
            toml_dict = tomllib.load(toml)

        host, port = toml_dict["service"].split(":")
        port = int(port)

        username = toml_dict["username"]
        password = toml_dict["password"]

        debug = toml_dict.get("debug", "")
    except FileNotFoundError:
        sys.exit(
            "conf.toml не найден!\n" "Поместите файл конфигурации в корень каталога"
        )
    except KeyError:
        sys.exit(
            "Недопустимый формат conf.toml!\n"
            "Проверьте наличие данных в следующем виде:\n"
            'service = "host:port"\n'
            'username = "username"\n'
            'password = "password"'
        )
    except Exception as e:
        sys.exit(f"Не удалось прочитать conf.toml!\n{e}")

    if debug.lower() == "true":
        log_level = "DEBUG"
    else:
        log_level = "INFO"

    with open("sms.log", "a"):
        pass

    logging.basicConfig(
        filename="sms.log", level=log_level, format="%(asctime)s | %(message)s"
    )

    logging.info(f'running | {sender} -> {recipient}: "{message}"')

    client = SocketSmsClient(host=host, port=port, username=username, password=password)

    try:
        response = client.send_sms(sender=sender, recipient=recipient, message=message)
        print(f"Код ответа: {response.status_code}")
        if response.status_code == 200:
            logging.info(f"server | {response.status_code}: {response.body}")
            print(f"Тело ответа:\n{response.body}")
        else:
            logging.info(f"server | {response.status_code}: FAIL")
    except Exception as e:
        # логирование уровней дебага и исключений реализовано в классе
        print(f"Не удалось установить соединение!\n{e}")
