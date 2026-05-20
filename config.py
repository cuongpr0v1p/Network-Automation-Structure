# ============================================================
# CAU HINH HE THONG
# ============================================================

# Telegram
TELEGRAM_TOKEN   = "8962499948:AAEkZmekC4Suzx-Xo61IECp9k21IQp9tWLk"
TELEGRAM_CHAT_ID = "7193277767"

# Thu muc
BACKUP_DIR = "/root/network-automation/backups/switches"
LOG_DIR    = "/root/network-automation/logs"
DRIFT_DIR  = "/root/network-automation/drift"

# Danh sach thiet bi
DEVICES = [
    {"name": "SW-SERVER", "ip": "10.120.99.247", "user": "cuongvdq", "pass": "cuongvdq", "enable": "cuongvdq", "type": "cisco"},
    {"name": "SW-CORE",   "ip": "10.120.99.249", "user": "cuongvdq", "pass": "cuongvdq", "enable": "cuongvdq", "type": "cisco"},
    {"name": "SW-DMZ",    "ip": "10.120.99.246", "user": "cuongvdq", "pass": "cuongvdq", "enable": "cuongvdq", "type": "cisco"},
    {"name": "SW-LAN",    "ip": "10.120.99.248", "user": "cuongvdq", "pass": "cuongvdq", "enable": "cuongvdq", "type": "cisco"},
]
VLAN_CONFIG = [
    {"id": 10,  "name": "USER"},
    {"id": 20,  "name": "SERVER"},
    {"id": 30,  "name": "DMZ"},
    {"id": 90,  "name": "WIFI_STAFF"},
    {"id": 91,  "name": "WIFI_GUEST"},
    {"id": 99,  "name": "MANAGEMENT"},
]
