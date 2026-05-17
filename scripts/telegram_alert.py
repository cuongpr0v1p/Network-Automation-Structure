import os
import urllib.request
import urllib.parse
import sys
from datetime import datetime

sys.path.insert(0, '/root/network-automation')

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def send_telegram(message):

    url = (
        "https://api.telegram.org/bot{}/sendMessage"
    ).format(TELEGRAM_TOKEN)

    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }).encode()

    try:

        req = urllib.request.Request(url, data=data)

        urllib.request.urlopen(req, timeout=10)

        return True

    except Exception as e:

        print("Telegram error: " + str(e))

        return False


def send_backup_file(message, filepath):

    boundary = "----WebKitFormBoundary"

    data = []

    data.append("--" + boundary)

    data.append(
        'Content-Disposition: form-data; name="chat_id"\r\n'
    )

    data.append(str(TELEGRAM_CHAT_ID))

    data.append("--" + boundary)

    data.append(
        'Content-Disposition: form-data; name="caption"\r\n'
    )

    data.append(message)

    data.append("--" + boundary)

    data.append(
        'Content-Disposition: form-data; '
        'name="document"; filename="{}"\r\n'
        'Content-Type: text/plain\r\n'
        .format(os.path.basename(filepath))
    )

    with open(filepath, "rb") as f:
        file_content = f.read()

    body = []

    for item in data:
        body.append(item.encode())

    body.append(file_content)

    body.append(
        ("--" + boundary + "--").encode()
    )

    body_bytes = b"\r\n".join(body)

    url = (
        "https://api.telegram.org/bot{}/sendDocument"
    ).format(TELEGRAM_TOKEN)

    req = urllib.request.Request(url)

    req.add_header(
        "Content-Type",
        "multipart/form-data; boundary={}".format(boundary)
    )

    try:

        urllib.request.urlopen(
            req,
            data=body_bytes,
            timeout=20
        )

        return True

    except Exception as e:

        print(
            "Telegram upload error: " + str(e)
        )

        return False


def alert_device_down(device_name, ip):

    msg = (
        "<b>CANH BAO HE THONG</b>\n"
        "Thoi gian  : {}\n"
        "Thiet bi   : <b>{}</b>\n"
        "IP         : {}\n"
        "Trang thai : DOWN\n"
        "Hanh dong  : Da bo qua backup"
    ).format(
        now(),
        device_name,
        ip
    )

    return send_telegram(msg)


def alert_backup_failed(device_name, ip, error):

    msg = (
        "<b>BACKUP THAT BAI</b>\n"
        "Thoi gian : {}\n"
        "Thiet bi  : <b>{}</b>\n"
        "IP        : {}\n"
        "Loi       : {}"
    ).format(
        now(),
        device_name,
        ip,
        error
    )

    return send_telegram(msg)


def alert_backup_success(device_name, results):

    lines = [
        "<b>BACKUP HOAN THANH</b>",
        "Thoi gian : {}".format(now()),
        "-"*30,
    ]

    for r in results:

        status = "OK" if r['ok'] else "FAILED"

        lines.append(
            "{} : {}".format(
                r['name'],
                status
            )
        )

    return send_telegram(
        "\n".join(lines)
    )


def alert_config_drift(device_name, changes):

    msg = (
        "<b>CONFIG THAY DOI</b>\n"
        "Thoi gian        : {}\n"
        "Thiet bi         : <b>{}</b>\n"
        "So dong thay doi : {}\n"
        "Vui long kiem tra ngay!"
    ).format(
        now(),
        device_name,
        changes
    )

    return send_telegram(msg)

