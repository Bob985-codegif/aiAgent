import asyncio
import os
import sys
from unittest.mock import patch

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.code_agent.agent.langgraph_code_agent import run_agent

async def test_agent_clone():
    """测试agent是否能直接执行git clone命令"""
    # 准备测试数据
    repo_url = "https://github.com/youlaitech/vue3-element-admin.git"
    target_dir = r"D:\BaiduNetdiskDownload\ai_agent_with_langchain\.code"
    test_input = f"将{repo_url}项目克隆到{target_dir}目录下"
    
    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    print(f"测试输入: {test_input}")
    print(f"目标目录: {target_dir}")
    
    # 使用mock替换input函数，返回预定义的测试输入
    with patch('builtins.input', side_effect=[test_input, "exit"]):
        try:
            await run_agent()
            print("✅ 测试完成")
        except Exception as e:
            print(f"❌ 测试过程中发生异常: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent_clone())
