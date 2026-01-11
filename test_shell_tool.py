import asyncio
import os

from app.code_agent.tools.shell_tools import get_stdio_shell_tools

async def test_shell_tool():
    """直接测试MCP shell工具"""
    print("获取shell工具...")
    shell_tools = await get_stdio_shell_tools()
    
    print(f"获取到{len(shell_tools)}个shell工具")
    for tool in shell_tools:
        print(f"工具名称: {tool.name}, 描述: {tool.description}")
    
    # 查找run_shell工具
    run_shell_tool = None
    for tool in shell_tools:
        if tool.name == "run_shell":
            run_shell_tool = tool
            break
    
    if not run_shell_tool:
        print("❌ 未找到run_shell工具")
        return False
    
    print("\n测试run_shell工具执行简单命令...")
    
    # 辅助函数：提取工具返回结果中的文本
    def extract_text(result):
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict) and 'text' in result[0]:
                return result[0]['text']
        return str(result)
    
    # 测试1: 执行cd命令（Windows系统）
    try:
        result = await run_shell_tool.ainvoke({"command": "cd"})
        text_result = extract_text(result)
        print(f"✅ cd命令执行成功: {text_result.strip()}")
    except Exception as e:
        print(f"❌ cd命令执行失败: {str(e)}")
        return False
    
    # 测试2: 执行dir命令
    try:
        result = await run_shell_tool.ainvoke({"command": "dir"})
        text_result = extract_text(result)
        print(f"✅ dir命令执行成功，输出前500字符: {text_result[:500]}...")
    except Exception as e:
        print(f"❌ dir命令执行失败: {str(e)}")
        return False
    
    # 测试3: 执行echo命令
    try:
        test_msg = "Hello, Shell Tool!"
        result = await run_shell_tool.ainvoke({"command": f"echo {test_msg}"})
        text_result = extract_text(result)
        if test_msg in text_result:
            print(f"✅ echo命令执行成功: {text_result.strip()}")
        else:
            print(f"❌ echo命令执行失败，预期包含'{test_msg}'，实际输出: {text_result}")
            return False
    except Exception as e:
        print(f"❌ echo命令执行失败: {str(e)}")
        return False
    
    # 测试4: 执行git --version命令
    try:
        result = await run_shell_tool.ainvoke({"command": "git --version"})
        text_result = extract_text(result)
        if "git version" in text_result:
            print(f"✅ git命令执行成功: {text_result.strip()}")
        else:
            print(f"⚠️ git命令执行结果不符合预期: {text_result.strip()}")
    except Exception as e:
        print(f"❌ git命令执行失败: {str(e)}")
        print("⚠️ 可能需要安装git或配置PATH环境变量")
    
    print("\n✅ 所有shell工具测试通过!")
    return True

if __name__ == "__main__":
    asyncio.run(test_shell_tool())
