import os
import sys
from datetime import datetime
sys.path.insert(0, '/root/network-automation')
from config import LOG_DIR

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def log(message, level="INFO"):
    today    = datetime.now().strftime("%Y-%m-%d")
    now      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = "{}/system_{}.log".format(LOG_DIR, today)
    line     = "[{}] [{}] {}".format(now, level, message)
    print(line)
    with open(log_file, "a") as f:
        f.write(line + "\n")

def log_info(msg):    log(msg, "INFO")
def log_ok(msg):      log(msg, "OK")
def log_warning(msg): log(msg, "WARNING")
def log_error(msg):   log(msg, "ERROR")
