# NETWORK AUTOMATION STRUCTURE

Hệ thống Network Automation được xây dựng trên nền tảng Ubuntu 16.04 sử dụng Python 3.5 với mục tiêu tự động hóa các tác vụ quản trị mạng trong môi trường doanh nghiệp.

---

# MỤC TIÊU DỰ ÁN

- Tự động hóa quá trình quản trị mạng
- Giảm thao tác cấu hình thủ công
- Backup cấu hình thiết bị tự động
- Giám sát trạng thái thiết bị mạng
- Phát hiện thay đổi cấu hình (Config Drift)
- Gửi cảnh báo tự động qua Telegram
- Quản lý lịch sử cấu hình bằng GitHub
- Hỗ trợ triển khai VLAN tự động

---
# DANH SÁCH THIẾT BỊ

| Tên thiết bị | IP Management | Loại | Ghi chú |
|---|---|---|---|
| FW_Active | 10.120.99.250 | FortiGate | Chỉ monitor, chưa backup |
| SW-CORE | 10.120.99.249 | Cisco IOSvL2 | Monitor + Backup |
| SW-DMZ | 10.120.99.246 | Cisco IOSvL2 | Monitor + Backup |
| SW-SERVER | 10.120.99.247 | Cisco IOSvL2 | Monitor + Backup |
| SW-LAN | 10.120.99.248 | Cisco IOSvL2 | Monitor + Backup |
# CÁC CHỨC NĂNG ĐÃ TRIỂN KHAI
---
## Device Monitoring
- Kiểm tra trạng thái thiết bị bằng ICMP Ping
- Phát hiện thiết bị UP/DOWN
- Tự động cảnh báo khi thiết bị mất kết nối

## Automatic Backup
- SSH vào Cisco Switch
- Tự động lấy `show running-config`
- Backup cấu hình theo thời gian thực
- Lưu file backup theo timestamp

## Config Drift Detection
- So sánh giữa 2 bản backup gần nhất
- Phát hiện thay đổi cấu hình
- Sinh drift report tự động

## Telegram Alert System
- Alert thiết bị DOWN
- Alert Backup FAILED
- Alert Config Drift
- Alert Backup SUCCESS

## GitHub Version Control
- Push backup tự động lên GitHub
- Lưu lịch sử cấu hình thiết bị mạng
- Hỗ trợ version control cho hệ thống

## VLAN Deployment
- Deploy VLAN tự động lên switch Cisco
- Tạo VLAN và save cấu hình

## Logging System
- Phân loại log theo chức năng
- Log rotate theo ngày
- Hỗ trợ audit & troubleshooting

---

# WORKFLOW TỔNG QUÁT

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
# FILE CẤU HÌNH & BACKUP

Toàn bộ file cấu hình backup của hệ thống được lưu trữ tại Google Drive:

📂 Google Drive Backup Repository:

:contentReference[oaicite:0]{index=0}

Bao gồm:
- File backup cấu hình switch
- Drift report
- Version backup
- File phục vụ audit & troubleshooting

---
