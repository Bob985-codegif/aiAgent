from app.code_agent.utils.mcp import create_mcp_stdio_client
import os
import sys


async def get_stdio_browser_tools():
    # 动态获取路径（兼容 Windows 和 Linux/macOS）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    browser_tools_path = os.path.abspath(
        os.path.join(
            current_dir,
            '..',  
            'mcp',
            'browser_tools.py'  # 进入 mcp 目录
        ))

    # 规范化路径
    browser_tools_path = os.path.normpath(browser_tools_path)

    print(f"📂 浏览器工具路径: {browser_tools_path}")
    print(f"✓ 文件存在: {os.path.exists(browser_tools_path)}")

    if not os.path.exists(browser_tools_path):
        raise FileNotFoundError(f"找不到浏览器工具文件: {browser_tools_path}")

    params = {"command": sys.executable, "args": [browser_tools_path]}

    client, tools = await create_mcp_stdio_client("browser_tools", params)

    return tools
