import sys
sys.path.insert(0, '/root/network-automation')

from config import DEVICES
from scripts.deploy_vlan import get_vlan_input, choose_switches, deploy_all
from scripts.logger import log_ok, log_error

# Nhap thong tin VLAN
vlans = get_vlan_input()

if not vlans:
    print("Khong co VLAN nao duoc nhap. Thoat.")
    sys.exit(0)

# Hien thi tom tat
print("\n" + "="*50)
print("TOM TAT VLAN SE DEPLOY:")
print("-"*50)
for v in vlans:
    print("  VLAN {:4d} -- {}".format(v['id'], v['name']))
print("="*50)

# Chon switch
selected = choose_switches(DEVICES)

if not selected:
    print("Khong co switch nao duoc chon. Thoat.")
    sys.exit(0)

print("\nSwitch se deploy:")
for s in selected:
    print("  - {} ({})".format(s['name'], s['ip']))

confirm = input("\nXac nhan deploy? (y/n): ").strip().lower()
if confirm != 'y':
    print("Da huy.")
    sys.exit(0)

# Bat dau deploy
print("\n" + "="*50)
print("BAT DAU DEPLOY...")
print("="*50)
results = deploy_all(selected, vlans)

# Ket qua
print("\n" + "="*50)
print("KET QUA:")
print("-"*50)
for r in results:
    status = "OK" if r['ok'] else "FAILED"
    print("  {} -- {}".format(r['name'], status))
print("="*50)
