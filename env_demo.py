import os
from dotenv import load_dotenv

# 演示环境变量的设置和获取方法

# 方法1：通过.env文件设置（最常用）
print("=== 方法1：通过.env文件设置环境变量 ===")
print(".env文件路径:", os.path.abspath(".env"))
print(".env文件内容:")
with open(".env", "r", encoding="utf-8") as f:
    print(f.read())

# 加载.env文件中的环境变量
load_dotenv()
print("\n加载后获取BAILIAN_API_KEY:", os.environ.get("BAILIAN_API_KEY"))

# 方法2：直接在代码中设置
print("\n=== 方法2：直接在代码中设置环境变量 ===")
os.environ["TEMP_VAR"] = "临时变量值"
print("设置的TEMP_VAR:", os.environ.get("TEMP_VAR"))

# 方法3：检查系统环境变量（Windows示例）
print("\n=== 方法3：系统环境变量示例 ===")
print("系统PATH环境变量前100个字符:", os.environ.get("PATH")[:100] + "...")
print("用户HOME环境变量:", os.environ.get("HOME"))

# 总结
print("\n=== 环境变量设置方法总结 ===")
print("1. 通过.env文件：适合项目特定的变量，方便管理")
print("2. 代码中设置：适合临时或动态变量")
print("3. 系统环境变量：适合全局使用的变量")
print("4. 命令行设置：适合一次性使用的变量")
