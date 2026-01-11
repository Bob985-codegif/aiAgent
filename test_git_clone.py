from app.code_agent.tools.file_tools import shell_tools
import asyncio

async def test_git_clone():
    print("🔍 获取 shell_tools...")
    print(f"📁 shell_tools: {shell_tools}")
    print(f"📁 工具类型: {type(shell_tools)}")
    print(f"📁 工具数量: {len(shell_tools)}")
    
    if not shell_tools:
        print("❌ 未找到 shell_tools")
        return
    
    shell_tool = shell_tools[0]
    print(f"🔧 使用的工具: {shell_tool}")
    print(f"🔧 工具名称: {shell_tool.name}")
    print(f"🔧 工具描述: {shell_tool.description}")
    
    # 测试简单的 shell 命令
    print("\n📝 测试简单 shell 命令...")
    try:
        result = await shell_tool.ainvoke("echo 'Hello, Git!'")
        print(f"✅ 命令执行成功: {result}")
    except Exception as e:
        print(f"❌ 命令执行失败: {e}")
        return
    
    # 测试 git clone 命令
    print("\n📝 测试 git clone 命令...")
    repo_url = "https://github.com/youlaitech/vue3-element-admin.git"
    target_dir = ".code/vue3-element-admin"
    
    try:
        # 先创建目标目录
        await shell_tool.ainvoke(f"mkdir -p {target_dir}")
        print("✅ 目标目录创建成功")
        
        # 执行 git clone 命令
        clone_cmd = f"git clone {repo_url} {target_dir}"
        print(f"📥 执行命令: {clone_cmd}")
        
        result = await shell_tool.ainvoke(clone_cmd)
        print(f"✅ 克隆成功: {result}")
        print("🎉 Git clone 功能测试通过!")
    except Exception as e:
        print(f"❌ 克隆失败: {e}")
        print("💡 可能的原因: 网络问题、Git 未安装、权限问题等")

if __name__ == "__main__":
    asyncio.run(test_git_clone())