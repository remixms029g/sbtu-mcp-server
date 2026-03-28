from mcp.server.fastmcp import FastMCP
import sqlite3
import subprocess
import shlex

# 1. เริ่มต้น Server ในชื่อ SBTUMCP
mcp = FastMCP("SBTUMCP")

# 2. จัดการฐานข้อมูล
DB_FILE = "sbtu_memory.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)")

init_db()

@mcp.tool()
def get_status() -> str:
    """เช็กสถานะระบบ SBTUMCP"""
    return "SBTUMCP Core is Online and Ready!"

# เพิ่ม Tool อื่นๆ (ADB/Ollama) ตามที่พี่บอลเขียนไว้ได้เลยครับ

if __name__ == "__main__":
    mcp.run()