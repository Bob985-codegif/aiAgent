#!/usr/bin/env python3
"""Code Agent 启动脚本

这个脚本解决了模块导入问题，确保Python能够正确找到'app'模块。
使用方法：
    python run_code_agent.py
"""
import os
import sys

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

# 将项目根目录添加到Python路径
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"🔧 添加项目根目录到Python路径: {project_root}")

# 导入并运行主程序
try:
    from app.code_agent.agent.code_agent import run_agent
    import asyncio
    
    print("🚀 启动 Code Agent...")
    asyncio.run(run_agent())
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("💡 确保已正确安装所有依赖:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ 运行错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)