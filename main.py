import sys
sys.path.insert(0, '/root/network-automation')

from config import DEVICES
from scripts.monitor        import check_devices
from scripts.backup         import backup_cisco
from scripts.config_drift   import check_all_drift
from scripts.telegram_alert import (
    alert_device_down, alert_backup_failed,
    alert_backup_success, alert_config_drift
)
from scripts.github_push import push_to_github
from scripts.logger import log_info, log_ok, log_warning, log_error

def run():
    log_info("="*50)
    log_info("BAT DAU NETWORK AUTOMATION")
    log_info("="*50)

    # ── STEP 1: CHECK ─────────────────────────────────
    log_info("STEP 1: Kiem tra trang thai thiet bi...")
    status_list  = check_devices(DEVICES)
    up_devices   = []
    down_devices = []

    for s in status_list:
        if s['up']:
            log_ok("  {} ({}) -- UP".format(s['name'], s['ip']))
            up_devices.append(s['name'])
        else:
            log_warning("  {} ({}) -- DOWN".format(s['name'], s['ip']))
            down_devices.append(s['name'])
            alert_device_down(s['name'], s['ip'])

    # ── STEP 2: BACKUP ────────────────────────────────
    log_info("STEP 2: Backup config...")
    backup_results = []

    for d in DEVICES:
        if d['name'] not in up_devices:
            log_warning("  Bo qua {}: DOWN".format(d['name']))
            continue
        ok, result, size = backup_cisco(d)
        if ok:
            log_ok("  {} -- OK -- {} bytes".format(d['name'], size))
            backup_results.append({"name": d['name'], "ok": True})
        else:
            log_error("  {} -- FAILED -- {}".format(d['name'], result))
            backup_results.append({"name": d['name'], "ok": False})
            alert_backup_failed(d['name'], d['ip'], result)

    if backup_results:
        alert_backup_success("He thong", backup_results)

    # ── STEP 2.5: PUSH GITHUB
    log_info("STEP 2.5: Push backup len GitHub...")
    push_to_github()

    # ── STEP 3: CONFIG DRIFT ──────────────────────────
    log_info("STEP 3: Kiem tra config drift...")
    drift_results = check_all_drift(DEVICES)

    for r in drift_results:
        if r['changed']:
            log_warning("  {} -- CO THAY DOI -- {} dong".format(
                r['name'], r['count']))

            if r['diff']['added']:
                log_warning("  >>> THEM MOI:")
                for line in r['diff']['added'][:5]:
                    log_warning("      + {}".format(line))

            if r['diff']['removed']:
                log_warning("  >>> DA XOA:")
                for line in r['diff']['removed'][:5]:
                    log_warning("      - {}".format(line))

            if r['drift_file']:
                log_warning("  >>> Bao cao drift: {}".format(r['drift_file']))

            alert_config_drift(r['name'], r['count'])
        else:
            log_ok("  {} -- Khong co thay doi".format(r['name']))

    # ── TONG KET ─────────────────────────────────────
    log_info("-"*50)
    log_info("Tong ket:")
    log_info("  Thiet bi UP      : {}".format(len(up_devices)))
    log_info("  Thiet bi DOWN    : {}".format(len(down_devices)))
    log_info("  Backup thanh cong: {}".format(
        sum(1 for r in backup_results if r['ok'])))
    log_info("  Config drift     : {}".format(
        sum(1 for r in drift_results if r['changed'])))
    log_info("="*60)

if __name__ == "__main__":
    run()
# Them import o dau file
