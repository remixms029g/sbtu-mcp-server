from mcp.server.fastmcp import FastMCP

# 1. ประกาศชื่อ Server ให้ระบบประมวลผล (และ AI) รู้จัก [Server Initialization]
mcp = FastMCP("SBTU_Master_Server")

# 2. สร้าง Tool ตัวแรกของระบบ (ให้ AI อย่างลี่ หรือพี่ซี เรียกใช้ได้) [Tool Definition]
@mcp.tool()
def get_sbtu_status() -> str:
    """ตรวจสอบสถานะการทำงานของระบบ SBTU Tech Ecosystem"""
    return "SBTU Local Server is online! Master Ball is in control."

if __name__ == "__main__":
    # 3. รันเซิร์ฟเวอร์ด้วยระบบ stdio ตามที่ตั้งใจไว้ [Execution Entry Point]
    mcp.run()