from app.code_agent.utils.mcp import create_mcp_stdio_client
import os


async def get_stdio_powershell_tools():
    # 动态获取路径（兼容 Windows 和 Linux/macOS）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    powershell_tools_path = os.path.abspath(
        os.path.join(
            current_dir,
            '..',  # 回到 app/code_agent
            'mcp', 'powershell_tools.py'  # 进入 mcp 目录
        )
    )
    
    # 规范化路径
    powershell_tools_path = os.path.normpath(powershell_tools_path)
    
    print(f"📂 PowerShell工具路径: {powershell_tools_path}")
    print(f"✓ 文件存在: {os.path.exists(powershell_tools_path)}")
    
    if not os.path.exists(powershell_tools_path):
        raise FileNotFoundError(f"找不到PowerShell工具文件: {powershell_tools_path}")
    
    params = {
        "command": "python",
        "args": [powershell_tools_path]
    }

    client, tools = await create_mcp_stdio_client("powershell_tools", params)

    return tools