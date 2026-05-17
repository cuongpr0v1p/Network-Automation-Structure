import subprocess
import os
import sys
from datetime import datetime
sys.path.insert(0, '/root/network-automation')
from config import BACKUP_DIR

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def backup_cisco(device):
    today = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = "{}/{}_{}.txt".format(BACKUP_DIR, device['name'], today)
    commands = "enable\n{}\nterminal length 0\nshow running-config\nend\n".format(
        device['enable'])
    cmd = [
        "sshpass", "-p", device['pass'],
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ConnectTimeout=10",
        "-tt",
        "{}@{}".format(device['user'], device['ip']),
    ]
    result = subprocess.run(
        cmd, input=commands.encode(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode == 0:
        config = result.stdout.decode('utf-8', errors='ignore')
        lines = config.splitlines()
        start = 0
        for i, line in enumerate(lines):
            if "Current configuration" in line:
                start = i
                break
        clean = "\n".join(lines[start:])
        with open(filename, 'w') as f:
            f.write(clean)
        size = os.path.getsize(filename)
        return True, filename, size
    else:
        err = result.stderr.decode('utf-8', errors='ignore').strip()
        return False, err, 0
