# Network Automation Structure

Hệ thống Network Automation được xây dựng trên Ubuntu 16.04 sử dụng Python 3.5 nhằm tự động hóa các tác vụ quản trị mạng trong môi trường doanh nghiệp.

---

## Features

- Device Monitoring (UP/DOWN)
- Automatic Backup Config
- Config Drift Detection
- Telegram Alert System
- GitHub Version Control
- VLAN Deployment
- Logging System

---

## Workflow

```text
Monitor
   ↓
Backup
   ↓
Push GitHub
   ↓
Config Drift
   ↓
Telegram Alert
   ↓
Deploy VLAN
   ↓
Logging System
