from app.code_agent.utils.mcp import create_mcp_stdio_client
import os


async def get_stdio_weather_tools():
    # 动态获取路径（兼容 Windows 和 Linux/macOS）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # current_dir = D:\BaiduNetdiskDownload\ai_agent_with_langchain\app\code_agent\tools
    weather_tools_path = os.path.abspath(
        os.path.join(
            current_dir,
            '..',  # 回到 D:\BaiduNetdiskDownload\ai_agent_with_langchain\app\code_agent
            'mcp', 'weather_tools.py'  # 直接进入 mcp 目录
        )
    )
    
    # 规范化路径
    weather_tools_path = os.path.normpath(weather_tools_path)
    
    print(f"📂 天气工具路径: {weather_tools_path}")
    print(f"✓ 文件存在: {os.path.exists(weather_tools_path)}")
    
    if not os.path.exists(weather_tools_path):
        raise FileNotFoundError(f"找不到天气工具文件: {weather_tools_path}")
    
    params = {
        "command": "python",
        "args": [weather_tools_path]
    }
    
    print(f"📋 天气工具执行参数: {params}")

    client, tools = await create_mcp_stdio_client("weather_tools", params)

    return tools
