from mcp.server.fastmcp import FastMCP
import sqlite3
import subprocess
import shlex
import os

# 1. เริ่มต้น Server ในชื่อ SBTUMCP
mcp = FastMCP("SBTUMCP")

# 2. จัดการฐานข้อมูล Memory
DB_FILE = "sbtu_memory.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)")

init_db()

# --- [ TOOLS ZONE ] ---

@mcp.tool()
def get_status() -> str:
    """เช็กสถานะระบบ SBTUMCP และรายงาน Path ปัจจุบัน"""
    current_path = os.getcwd()
    return f"SBTUMCP Core is Online and Ready! 🟢\nRunning from: {current_path}\nStatus: Master Ball is in control 🦞"

@mcp.tool()
async def run_adb_command(command: str) -> str:
    """สั่งงานมือถือ Android ผ่าน ADB (เช่น devices, shell input tap x y, screenshot)"""
    try:
        # ใช้ shlex เพื่อความปลอดภัยในการแยกคำสั่ง
        args = shlex.split(f"adb {command}")
        result = subprocess.run(args, capture_output=True, text=True, timeout=10)
        output = result.stdout if result.stdout else result.stderr
        return f"ADB Output:\n{output if output else 'Success (No output)'}"
    except Exception as e:
        return f"ADB Error: {str(e)}"

@mcp.tool()
async def ask_local_ollama(prompt: str, model: str = "llama3") -> str:
    """ส่งคำถามไปให้ Ollama ในเครื่องช่วยคิด (Offline AI)"""
    try:
        args = ["ollama", "run", model, prompt]
        result = subprocess.run(args, capture_output=True, text=True, timeout=60, encoding='utf-8')
        return f"Ollama ({model}) Response:\n{result.stdout}"
    except Exception as e:
        return f"Ollama Error: {str(e)}"

@mcp.tool()
async def save_memory(key: str, value: str) -> str:
    """บันทึกข้อมูลสำคัญลง SQLite Memory"""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
        return f"✅ บันทึก '{key}' ลงความจำเรียบร้อยแล้ว"
    except Exception as e:
        return f"Memory Error: {str(e)}"

@mcp.tool()
async def recall_memory(key: str) -> str:
    """ดึงความจำที่เคยบันทึกไว้ออกมา"""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.execute("SELECT value FROM memory WHERE key = ?", (key,))
            row = cursor.fetchone()
            return f"ความจำของ {key}: {row[0]}" if row else f"❌ ไม่พบความจำชื่อ {key}"
    except Exception as e:
        return f"Recall Error: {str(e)}"

# --- [ RUN SERVER ] ---

if __name__ == "__main__":
    mcp.run()
