#!/usr/bin/env python3
"""图书管理系统启动脚本"""

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
    from app_main import create_app
    
    print("📚 启动图书管理系统...")
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
    
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