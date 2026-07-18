# SBTU MCP Server Documentation

สำหรับเชื่อม Claude Desktop กับ GitHub ใช้จัดการ SBTU Tech repositories

## ภาพรวม

SBTU MCP Server เป็น Model Context Protocol server ที่ช่วยให้ Claude Desktop สามารถ:
- เข้าถึง GitHub repositories
- จัดการ code changes
- ทำ pull requests
- จัดการ issues

## ขั้นตอนการติดตั้ง

### ความต้องการ
- Python 3.10+
- GitHub Personal Access Token

### การติดตั้ง

```bash
git clone https://github.com/remixms029g/sbtu-mcp-server.git
cd sbtu-mcp-server
pip install -e .
```

### การตั้งค่า Claude Desktop

1. เปิดไฟล์ config ของ Claude Desktop
2. เพิ่ม MCP server configuration
3. ใส่ GitHub token ของคุณ
4. รีสตาร์ท Claude Desktop

## การใช้งาน

### คำสั่งพื้นฐาน

```bash
# ทดสอบการเชื่อมต่อ
python -m sbtu_mcp_server --test

# รัน server
python -m sbtu_mcp_server
```

### ตัวอย่างการใช้งาน

- สร้าง Pull Request อัตโนมัติ
- อ่านและเขียน Issues
- จัดการ Branches
- รีวิว Code Changes

## คุณสมบัติหลัก

- 🔗 **GitHub Integration** - เชื่อมต่อกับ GitHub API
- 🤖 **Claude AI** - ใช้ AI ในการจัดการ repositories
- 📱 **Cross-Platform** - ทำงานบน Windows, macOS, Linux
- 🚀 **Automation** - อัตโนมัติหลายขั้นตอน
- 🔐 **Secure** - ปลอดภัยด้วยการเข้ารหัส token

## Troubleshooting

### ปัญหา: Token ไม่ถูกต้อง
**วิธีแก้:** ตรวจสอบว่า token มี permission ที่ถูกต้องใน GitHub settings

### ปัญหา: ไม่สามารถเชื่อมต่อกับ GitHub
**วิธีแก้:** ตรวจสอบอินเทอร์เน็ต และ token ใหม่

## ลิงก์เพิ่มเติม

- [GitHub Repository](https://github.com/remixms029g/sbtu-mcp-server)
- [README](../README.md)
- [Development Log](../DEVELOPMENT_LOG.md)
- [MIT License](../LICENSE)
