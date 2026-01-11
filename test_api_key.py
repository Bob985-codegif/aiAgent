import os
from dotenv import load_dotenv

# 加载.env文件
print(f"当前工作目录: {os.getcwd()}")
print(f".env文件存在: {os.path.exists('.env')}")
load_dotenv()

# 检查环境变量
print(f"BAILIAN_API_KEY已设置: {'BAILIAN_API_KEY' in os.environ}")
print(f"OPENAI_API_KEY已设置: {'OPENAI_API_KEY' in os.environ}")
if 'BAILIAN_API_KEY' in os.environ:
    print(f"BAILIAN_API_KEY值: {os.environ['BAILIAN_API_KEY'][:5]}..." if len(os.environ['BAILIAN_API_KEY']) > 5 else os.environ['BAILIAN_API_KEY'])

# 尝试简单初始化模型
from langchain_openai import ChatOpenAI
try:
    print("尝试初始化ChatOpenAI...")
    llm = ChatOpenAI(
        model="qwen3-coder-plus",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.environ.get("BAILIAN_API_KEY"),
        streaming=True,
    )
    print("ChatOpenAI初始化成功!")
except Exception as e:
    print(f"初始化失败: {e}")
