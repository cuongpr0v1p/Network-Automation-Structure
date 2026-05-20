import subprocess
import sys
sys.path.insert(0, '/root/network-automation')

def get_vlan_input():
    vlans = []
    print("\n" + "="*50)
    print("  DEPLOY VLAN LEN SWITCH")
    print("="*50)
    print("Nhap thong tin VLAN can deploy.")
    print("Nhap 'done' khi xong.\n")

    while True:
        vlan_id = input("VLAN ID (hoac 'done' de ket thuc): ").strip()
        if vlan_id.lower() == 'done':
            break
        if not vlan_id.isdigit():
            print("  Vui long nhap so!")
            continue
        if int(vlan_id) < 1 or int(vlan_id) > 4094:
            print("  VLAN ID phai tu 1 den 4094!")
            continue
        vlan_name = input("Ten VLAN {}: ".format(vlan_id)).strip()
        if not vlan_name:
            print("  Ten VLAN khong duoc de trong!")
            continue
        vlans.append({"id": int(vlan_id), "name": vlan_name})
        print("  Da them VLAN {} - {}\n".format(vlan_id, vlan_name))

    return vlans

def build_vlan_commands(device, vlans):
    cmds = [
        "enable",
        device['enable'],
        "configure terminal"
    ]
    for v in vlans:
        cmds.append("vlan {}".format(v['id']))
        cmds.append(" name {}".format(v['name']))
    cmds.append("end")
    cmds.append("write memory")
    cmds.append("")
    return "\n".join(cmds)

def deploy_vlan_to_switch(device, vlans):
    commands = build_vlan_commands(device, vlans)
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
    return result.returncode == 0

def choose_switches(devices):
    print("\nChon switch can deploy:")
    print("0. Tat ca switch")
    for i, d in enumerate(devices):
        print("{}. {} ({})".format(i+1, d['name'], d['ip']))

    choice = input("\nNhap lua chon (vd: 0 hoac 1,2,3): ").strip()

    if choice == "0":
        return devices

    selected = []
    for c in choice.split(","):
        c = c.strip()
        if c.isdigit():
            idx = int(c) - 1
            if 0 <= idx < len(devices):
                selected.append(devices[idx])
    return selected

def deploy_all(devices, vlans):
    results = []
    for d in devices:
        print("  Dang deploy len {}...".format(d['name']), end=" ")
        ok = deploy_vlan_to_switch(d, vlans)
        if ok:
            print("OK")
        else:
            print("FAILED")
        results.append({"name": d['name'], "ok": ok})
    return results
