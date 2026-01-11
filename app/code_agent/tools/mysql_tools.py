"""MySQL工具模块，提供获取MySQL工具的功能"""
import os
from app.code_agent.utils.mcp import create_mcp_stdio_client

async def get_stdio_mysql_tools():
    """获取标准输入输出MySQL工具
    
    Returns:
        list: MySQL工具列表
    """
    # 动态获取路径（兼容 Windows 和 Linux/macOS）
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 直接使用绝对路径，避免多层嵌套的dirname调用
    mysql_tools_path = os.path.abspath(
        os.path.join(
            current_dir,
            '..',
            'mcp',
            'mysql_tools.py'
        )
    )

    # 规范化路径（处理 Windows 反斜杠）
    mysql_tools_path = os.path.normpath(mysql_tools_path)
    print(f"📂 MySQL工具路径: {mysql_tools_path}")
    print(f"✓ 文件存在: {os.path.exists(mysql_tools_path)}")
    print(f"✓  路径长度: {len(mysql_tools_path)}")

    if not os.path.exists(mysql_tools_path):
        raise FileNotFoundError(f"找不到 MySQL 工具文件: {mysql_tools_path}")

    # 使用安全的路径传递方式
    params = {
        "command": "python",
        "args": [mysql_tools_path]
    }

    print(f"📋 执行参数: {params}")

    _, tools = await create_mcp_stdio_client("mysql_tools", params)
    return tools