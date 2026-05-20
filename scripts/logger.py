import os
import sys
from datetime import datetime

sys.path.insert(0, '/root/network-automation')

from config import LOG_DIR


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def write_log(log_type, message, level="INFO"):

    today = datetime.now().strftime("%Y-%m-%d")

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    logfile = (
        "{}/{}_{}.log"
    ).format(
        LOG_DIR,
        log_type,
        today
    )

    line = "[{}] [{}] {}".format(
        now,
        level,
        message
    )

    print(line)

    with open(logfile, "a") as f:
        f.write(line + "\n")


# =========================================================
# SYSTEM LOG
# =========================================================

def log_info(msg):

    write_log(
        "system",
        msg,
        "INFO"
    )


def log_ok(msg):

    write_log(
        "system",
        msg,
        "OK"
    )


def log_warning(msg):

    write_log(
        "system",
        msg,
        "WARNING"
    )


def log_error(msg):

    write_log(
        "system",
        msg,
        "ERROR"
    )


# =========================================================
# MONITOR LOG
# =========================================================

def monitor_log(msg):

    write_log(
        "monitor",
        msg,
        "INFO"
    )


# =========================================================
# BACKUP LOG
# =========================================================

def backup_log(msg):

    write_log(
        "backup",
        msg,
        "INFO"
    )


# =========================================================
# DRIFT LOG
# =========================================================

def drift_log(msg):

    write_log(
        "drift",
        msg,
        "INFO"
    )


# =========================================================
# DEPLOY LOG
# =========================================================

def deploy_log(msg):

    write_log(
        "deploy",
        msg,
        "INFO"
    )


# =========================================================
# TELEGRAM LOG
# =========================================================

def telegram_log(msg):

    write_log(
        "telegram",
        msg,
        "INFO"
    )
