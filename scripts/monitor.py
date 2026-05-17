import subprocess
import sys
sys.path.insert(0, '/root/network-automation')

def ping(ip):
    result = subprocess.run(
        ["ping", "-c", "2", "-W", "1", ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.returncode == 0

def check_devices(devices):
    results = []
    for d in devices:
        is_up = ping(d['ip'])
        results.append({
            "name": d['name'],
            "ip":   d['ip'],
            "up":   is_up
        })
    return results
