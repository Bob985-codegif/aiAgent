# 导入必要的库
import os
from dotenv import load_dotenv

# 确保.env文件被加载 - 这是解决API密钥问题的关键
load_dotenv()
print("环境变量已加载")

# 直接导入所需模块而不是从site-packages导入
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 创建提示词模板
multi_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位优秀的技术专家，擅长解决各种开发中的技术问题"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# 创建LLM实例 - 使用环境变量中的API密钥
llm_qwen = ChatOpenAI(
    model="qwen3-coder-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.environ.get("BAILIAN_API_KEY"),
)

# 创建链
chain = multi_chat_prompt | llm_qwen

# 测试调用
print("\n开始测试...")
try:
    # 准备参数
    params = {"question": "你好，你是谁？", "chat_history": []}
    print(f"参数: {params}")

    # 使用invoke方法
    response = chain.invoke(params)
    print(f"响应成功: {response.content}")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
