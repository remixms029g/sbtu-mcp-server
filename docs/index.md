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

## การใช้งาน

ตั้งค่า Claude Desktop เพื่อใช้ MCP server นี้

## ลิงก์เพิ่มเติม

- [GitHub Repository](https://github.com/remixms029g/sbtu-mcp-server)
- [README](../README.md)
