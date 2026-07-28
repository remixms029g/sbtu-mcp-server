from mcp.server.fastmcp import FastMCP
import subprocess
import shlex
import os

# 1. เริ่มต้น Server ในชื่อ SBTUMCP
mcp = FastMCP("SBTUMCP")


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
    """ส่งคำถามไปให้ Ollama ในเครื่องช่วยคิด (Offline AI) ผ่าน REST API และรองรับ CLI Fallback"""
    import httpx
    try:
        # พยายามเชื่อมต่อผ่าน Ollama REST API แบบ Async (ไม่บล็อกเทรดหลัก)
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            data = response.json()
            return f"Ollama ({model}) Response:\n{data.get('response', '')}"
    except Exception as e:
        # หาก REST API มีปัญหา ให้ใช้ subprocess.run เป็น Fallback สำรอง
        try:
            args = ["ollama", "run", model, prompt]
            result = subprocess.run(args, capture_output=True, text=True, timeout=120, encoding='utf-8')
            if result.returncode == 0:
                return f"Ollama ({model}) Response (CLI Fallback):\n{result.stdout}"
            else:
                return f"Ollama API Error: {str(e)}\nCLI Fallback Error: {result.stderr}"
        except Exception as fallback_e:
            return f"Ollama API Error: {str(e)}\nCLI Fallback Error: {str(fallback_e)}"


# --- [ RUN SERVER ] ---

if __name__ == "__main__":
    mcp.run()