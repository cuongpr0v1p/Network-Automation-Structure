import os, sys, glob
from datetime import datetime
sys.path.insert(0, '/root/network-automation')
from config import BACKUP_DIR, DRIFT_DIR

if not os.path.exists(DRIFT_DIR):
    os.makedirs(DRIFT_DIR)

def get_latest_two(device_name):
    files = sorted(glob.glob("{}/{}_*.txt".format(BACKUP_DIR, device_name)))
    if len(files) >= 2:
        return files[-2], files[-1]   # file truoc va file moi nhat
    return None, None

def filter_lines(lines):
    ignore = [
        "Current configuration",
        "Last configuration change",
        "NVRAM config last updated",
    ]
    result = []
    for l in lines:
        skip = any(ig in l for ig in ignore)
        if not skip:
            result.append(l)
    return result

def compare_configs(device_name):
    old_file, new_file = get_latest_two(device_name)
    if not old_file:
        return False, 0, {}, old_file, new_file

    with open(old_file) as f:
        old_set = set(filter_lines(f.readlines()))
    with open(new_file) as f:
        new_set = set(filter_lines(f.readlines()))

    added   = [l.strip() for l in (new_set - old_set) if l.strip()]
    removed = [l.strip() for l in (old_set - new_set) if l.strip()]
    changes = len(added) + len(removed)

    return changes > 0, changes, {"added": added, "removed": removed}, old_file, new_file

def save_drift_report(device_name, diff, old_file, new_file):
    today    = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = "{}/{}_drift_{}.txt".format(DRIFT_DIR, device_name, today)
    with open(filename, 'w') as f:
        f.write("="*60 + "\n")
        f.write("CONFIG DRIFT REPORT\n")
        f.write("="*60 + "\n")
        f.write("Thiet bi  : {}\n".format(device_name))
        f.write("Thoi gian : {}\n".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        f.write("Backup cu : {}\n".format(os.path.basename(old_file)))
        f.write("Backup moi: {}\n".format(os.path.basename(new_file)))
        f.write("="*60 + "\n\n")
        if diff['added']:
            f.write("[ DONG DUOC THEM MOI ]\n" + "-"*40 + "\n")
            for line in diff['added']:
                f.write("+ {}\n".format(line))
        if diff['removed']:
            f.write("\n[ DONG DA BI XOA ]\n" + "-"*40 + "\n")
            for line in diff['removed']:
                f.write("- {}\n".format(line))
        f.write("\n" + "="*60 + "\n")
        f.write("Tong thay doi: {}\n".format(
            len(diff['added']) + len(diff['removed'])))
    return filename

def check_all_drift(devices):
    results = []
    for d in devices:
        changed, count, diff, old_f, new_f = compare_configs(d['name'])
        drift_file = save_drift_report(
            d['name'], diff, old_f, new_f) if changed else None
        results.append({
            "name": d['name'], "changed": changed,
            "count": count, "diff": diff,
            "old": old_f, "new": new_f,
            "drift_file": drift_file
        })
    return results
