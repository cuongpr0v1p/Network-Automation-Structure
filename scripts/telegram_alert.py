import urllib.request
import urllib.parse
import sys
import time
from datetime import datetime
sys.path.insert(0, '/root/network-automation')
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_telegram(message, retry=3):
    url  = "https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_TOKEN)
    data = urllib.parse.urlencode({
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       message,
        "parse_mode": "HTML"
    }).encode()
    for attempt in range(1, retry+1):
        try:
            req  = urllib.request.Request(url, data=data)
            urllib.request.urlopen(req, timeout=15)
            return True
        except Exception as e:
            print("Telegram attempt {}/{}: {}".format(attempt, retry, str(e)))
            if attempt < retry:
                time.sleep(3)
    return False

def alert_device_down(device_name, ip):
    return send_telegram((
        "<b>CANH BAO HE THONG</b>\n"
        "Thoi gian  : {}\n"
        "Thiet bi   : <b>{}</b>\n"
        "IP         : {}\n"
        "Trang thai : DOWN\n"
        "Hanh dong  : Da bo qua backup"
    ).format(now(), device_name, ip))

def alert_backup_failed(device_name, ip, error):
    return send_telegram((
        "<b>BACKUP THAT BAI</b>\n"
        "Thoi gian : {}\n"
        "Thiet bi  : <b>{}</b>\n"
        "IP        : {}\n"
        "Loi       : {}"
    ).format(now(), device_name, ip, error))

def alert_backup_success(device_name, results):
    lines = ["<b>BACKUP HOAN THANH</b>", "Thoi gian : {}".format(now()), "-"*30]
    for r in results:
        lines.append("{} : {}".format(r['name'], "OK" if r['ok'] else "FAILED"))
    return send_telegram("\n".join(lines))

def alert_config_drift(device_name, changes, added=None, removed=None):
    lines = [
        "<b>CONFIG THAY DOI</b>",
        "Thoi gian        : {}".format(now()),
        "Thiet bi         : <b>{}</b>".format(device_name),
        "So dong thay doi : {}".format(changes),
    ]
    if added:
        lines.append("\nTHEM MOI:")
        for l in added[:3]:
            lines.append("+ {}".format(l))
    if removed:
        lines.append("\nDA XOA:")
        for l in removed[:3]:
            lines.append("- {}".format(l))
    lines.append("\nVui long kiem tra ngay!")
    return send_telegram("\n".join(lines))
