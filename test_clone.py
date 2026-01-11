import asyncio
from app.code_agent.agent.langgraph_code_agent import run_agent


async def test_clone():
    # 这里我们需要修改run_agent函数，使其支持非交互式调用
    # 或者创建一个新的函数来测试克隆功能
    import os
    import subprocess

    # 直接测试git clone命令
    repo_url = "https://github.com/youlaitech/vue3-element-admin.git"
    target_dir = r"D:\BaiduNetdiskDownload\ai_agent_with_langchain\.code"

    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 运行git clone命令
    command = f"git clone {repo_url} {target_dir}"
    print(f"运行命令: {command}")

    try:
        result = subprocess.run(command,
                                shell=True,
                                capture_output=True,
                                text=True)

        if result.returncode == 0:
            print("✅ 克隆成功!")
            print(f"输出: {result.stdout}")
        else:
            print(f"❌ 克隆失败，返回码: {result.returncode}")
            print(f"错误信息: {result.stderr}")
    except Exception as e:
        print(f"❌ 克隆过程中发生异常: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_clone())
