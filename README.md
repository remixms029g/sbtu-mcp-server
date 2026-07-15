# SBTU-MCP-SERVER

MCP (Model Context Protocol) server สำหรับ **SBTU Tech Ecosystem** — สะพานเชื่อมระหว่าง AI Agent (Claude, Gemini CLI) กับ Android device, Termux, และ local AI infrastructure ผ่าน Tailscale mesh

*Developed by Master Ball (Bridge Master) for SBTU Technology Infrastructure.*

---

## ภาพรวม (Overview)

sbtu-mcp-server เป็น MCP server ที่รันบน Windows PC (`sbtu`, node หลักใน Tailscale mesh) ทำหน้าที่เป็นตัวกลางให้ AI agent ภายนอก (เช่น Claude Desktop ผ่าน MCP protocol) สามารถ:

- สั่งงาน Android device ผ่าน ADB
- เรียกใช้ local LLM ผ่าน Ollama โดยไม่ต้องพึ่ง cloud
- (แผน) เก็บ context/memory แบบ persistent ผ่าน SQLite

Server ตัวนี้เป็นส่วนหนึ่งของ **AI Trinity architecture** — ทำงานร่วมกับ Claude (พี่บริดจ์), Gemini CLI (น้องลี่), See AI (พี่ซี) โดยแต่ละตัวรักษา Identity Independence ไม่ merge role กัน

---

## สถาปัตยกรรม (Architecture)

```
┌─────────────────┐         MCP Protocol          ┌──────────────────────┐
│  Claude Desktop  │ ◄────────────────────────────► │   sbtu-mcp-server     │
│  (หรือ MCP client)│                                │   (FastMCP, Python)   │
└─────────────────┘                                └──────────┬───────────┘
                                                                │
                                    ┌───────────────────────────┼───────────────────────────┐
                                    │                            │                            │
                              subprocess                   subprocess                   (แผน)
                              (adb CLI)                   (ollama CLI)                 sqlite3
                                    │                            │                            │
                                    ▼                            ▼                            ▼
                          ┌──────────────────┐         ┌──────────────────┐        ┌──────────────────┐
                          │  Android device   │         │  Ollama (local)   │        │  memory.db         │
                          │  (ผ่าน ADB/USB     │         │  localhost:11434  │        │  (key-value store) │
                          │  หรือ Tailscale)   │         │                    │        │  ยังไม่ได้เชื่อมต่อ │
                          └──────────────────┘         └──────────────────┘        └──────────────────┘
```

**Tech stack:** Python ≥3.13, [FastMCP](https://github.com/modelcontextprotocol/python-sdk) (`mcp[cli]>=1.26.0`), package management ผ่าน `uv`

---

## Features (Tools ที่มีอยู่ตอนนี้)

### `get_status()`
เช็คสถานะระบบ คืนค่า current working directory และข้อความยืนยันว่า server online

**สถานะ:** ✅ ทำงานสมบูรณ์

### `run_adb_command(command: str)`
รันคำสั่ง ADB ตามที่ระบุ (เช่น `devices`, `shell input tap x y`, `shell screencap`) โดยต่อท้าย `adb ` แล้ว execute ผ่าน `subprocess.run` (แยกคำสั่งด้วย `shlex` เพื่อความปลอดภัยระดับ shell-injection)

**สถานะ:** ✅ ทำงานได้ | ⚠️ เป็น **generic passthrough** — รับคำสั่ง ADB อะไรก็ได้ที่ผ่านมา ไม่มี allow-list จำกัดขอบเขต ใครก็ตามที่เรียก tool นี้ได้เท่ากับมีสิทธิ์ควบคุม ADB เต็มรูปแบบ

### `ask_local_ollama(prompt: str, model: str = "llama3")`
ส่ง prompt ไปยัง Ollama ที่รันในเครื่องเดียวกัน

**สถานะ:** ⚠️ **มี known bug** — ปัจจุบันเรียกผ่าน `subprocess.run(["ollama", "run", model, prompt], timeout=120)` ซึ่งเป็นการเรียก Ollama CLI แบบ blocking process มีปัญหา timeout ไม่เสถียรกับ prompt ยาวหรือ model โหลดช้า

**แนวทางแก้ที่วางแผนไว้:** เปลี่ยนไปใช้ `httpx.AsyncClient` เรียก REST API ตรงที่ `http://localhost:11434/api/generate` (`stream: False`) แทน — ต้องเพิ่ม `httpx` เข้า `pyproject.toml` dependencies ก่อน (ปัจจุบันยังไม่มี)

---

## ส่วนที่วางแผนไว้แต่ยังไม่เสร็จ

### SQLite Context Store — ❌ ยังไม่ทำงาน

`src/sbtumcp/__init__.py` มีโค้ดร่างไว้:

```python
conn.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        key TEXT PRIMARY KEY,
        value TEXT
    )
""")
conn.commit()
```

**ปัญหาปัจจุบัน:** ไฟล์นี้ไม่มี `import sqlite3` และไม่มีการประกาศตัวแปร `conn` — โค้ดนี้จะ throw `NameError` ทันทีถ้าถูกเรียก และ `main.py` ก็ยังไม่ได้ import อะไรจาก `sbtumcp` package ด้วยซ้ำ ต้องเขียนใหม่ทั้งการเชื่อมต่อ DB และเชื่อมเข้ากับ `main.py`

### ShizuWall Broadcast Integration — ❌ ยังไม่มีในโค้ด

เป้าหมาย: เพิ่ม tool ที่ยิง ADB broadcast ผ่าน action `shizuwall.CONTROL` เพื่อควบคุม ShizuWall (Hybrid Mode) บน OPPO A77 5G จาก MCP server โดยตรง — ยังไม่ได้เริ่มพัฒนา

### Deploy / Docker — ✅ มีเรียบร้อยแล้ว (อัปเดตผ่าน Dockerfile)

มี `Dockerfile` เรียบร้อยแล้วในโปรเจกต์ ซึ่งสามารถนำไปประกอบการทำงานคู่กับ Docker Desktop บน `sbtu` ได้ทันที (อ่านวิธีการใช้งานได้ในหัวข้อ [Docker usage](#docker-usage) ด้านล่าง)

---

## Quick Start (การติดตั้ง)

ต้องมี Python ≥3.13 และ [uv](https://github.com/astral-sh/uv) ติดตั้งไว้ก่อน

```bash
git clone https://github.com/remixms029g/sbtu-mcp-server.git
cd sbtu-mcp-server
uv sync
```

### Quick Start ตัวอย่าง
รันเซิร์ฟเวอร์แบบง่ายผ่าน stdio:
```bash
uv run src/sbtumcp/main.py
```

### Requirements ภายนอกที่ต้องมี (ไม่ได้ manage ผ่าน pyproject.toml)

- `adb` ต้องอยู่ใน PATH (สำหรับ `run_adb_command`)
- `ollama` ต้องรันอยู่ (สำหรับ `ask_local_ollama`) — ปัจจุบันเรียกผ่าน CLI, ในอนาคตจะเปลี่ยนเป็นเรียก REST API ที่ `localhost:11434`

---

## Claude Desktop config

เพิ่มคอนฟิกเพื่อเปิดใช้เซิร์ฟเวอร์ sbtu-mcp-server ร่วมกับแอปพลิเคชัน **Claude Desktop** ในไฟล์:
* **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
* **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

### ตัวอย่างการตั้งค่า (Claude Desktop config Example)
```json
{
  "mcpServers": {
    "sbtu-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/sbtu-mcp-server",
        "run",
        "python",
        "src/sbtumcp/main.py"
      ]
    }
  }
}
```

---

## Docker usage

คุณสามารถรันเซิร์ฟเวอร์ MCP นี้ในคอนเทนเนอร์ด้วย Docker ตามตัวอย่างคำสั่งนี้:

### 1. Build Docker Image
```bash
docker build -t sbtu-mcp-server:latest .
```

### 2. รันเพื่อทดสอบ stdio
```bash
docker run -i --rm sbtu-mcp-server:latest
```

---

## ตัวอย่างการเรียก tool

ตัวอย่างโครงสร้างคำสั่งและการส่งข้อมูลเพื่อเรียกใช้งานเครื่องมือ (Tools) ในเซิร์ฟเวอร์นี้:

* **`get_status()`**: เช็กสถานะการเชื่อมต่อออนไลน์และโฟลเดอร์ทำงานปัจจุบัน
  ```json
  get_status()
  ```
* **`run_adb_command(command)`**: รันคำสั่งผ่าน ADB เช่น ตรวจสอบรายการอุปกรณ์ที่เชื่อมต่อ
  ```json
  run_adb_command(command: "devices")
  ```
* **`ask_local_ollama(prompt, model)`**: ส่งข้อคำถามประมวลผลกับปัญญาประดิษฐ์ท้องถิ่น (Ollama)
  ```json
  ask_local_ollama(prompt: "Explain MCP in one sentence", model: "gemma3-1b-gpu-custom")
  ```

---

## Dependencies

```toml
[project]
requires-python = ">=3.13"
dependencies = [
    "mcp[cli]>=1.26.0",
]
```

**หมายเหตุ:** `httpx` ยังไม่อยู่ใน dependency list — ต้องเพิ่มก่อนแก้ bug ของ `ask_local_ollama`

---

## Roadmap (ลำดับที่เสนอไว้ ยังไม่ตัดสินใจ)

| ลำดับ | งาน | เหตุผล |
|---|---|---|
| 1 | แก้ `ask_local_ollama` ให้ใช้ httpx แทน subprocess | เป็น blocker ที่รู้อยู่แล้ว ฟีเจอร์อื่นที่ต่อยอดจาก Ollama bridge จะพังตามถ้าไม่แก้ |
| 2 | เชื่อม SQLite context store เข้ากับ `main.py` จริง | ปัจจุบันเป็นโค้ดลอย ไม่ทำงาน |
| 3 | เพิ่ม `shizuwall.CONTROL` broadcast tool | ต่อยอดจาก ShizuWall ที่ตั้งค่าเสร็จแล้วบน A77 5G |
| 4 | เพิ่ม Dockerfile/compose.yaml | รวม deploy เข้ากับ Docker Desktop stack บน `sbtu` |

---

## Ecosystem Context

| Node (Tailscale) | Role |
|---|---|
| `sbtu` (Windows PC) | รัน sbtu-mcp-server, Docker Desktop, Ollama |
| `oppo-a77-5g` | Primary Android — ShizuWall, Termux, Gemini CLI |
| `cph1819` (OPPO F7) | Secondary/reference Android |

Philosophy: **"Equal Brains, Unequal Wisdom"** — เรียนรู้ผ่านการลงมือทำ, Human in the Loop เสมอ

## License MIT
