import subprocess
import os
import sys
from datetime import datetime
sys.path.insert(0, '/root/network-automation')
from scripts.logger import log_info, log_ok, log_error

BACKUP_DIR = "/root/network-automation/backups"

def push_to_github():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_info("Push backup len GitHub...")

    try:
        os.chdir(BACKUP_DIR)

        # Git add
        subprocess.run(
            ["git", "add", "."],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Git commit
        msg = "Backup tu dong - {}".format(now)
        result = subprocess.run(
            ["git", "commit", "-m", msg],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        output = result.stdout.decode('utf-8', errors='ignore')

        # Neu khong co gi moi thi thoi
        if "nothing to commit" in output:
            log_info("  Khong co file moi, bo qua push")
            return True

        # Git push
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        if result.returncode == 0:
            log_ok("  Push GitHub: OK")
            return True
        else:
            err = result.stderr.decode('utf-8', errors='ignore')
            log_error("  Push GitHub: FAILED - " + err)
            return False

    except Exception as e:
        log_error("  Push GitHub loi: " + str(e))
        return False
