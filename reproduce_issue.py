
import sys
import os

# Add the project root to sys.path so we can import app
sys.path.append(os.getcwd())

from app.code_agent.mcp.shell_tools import run_shell_command

def test_clone():
    repo_url = "https://gitee.com/youlaiorg/vue3-element-admin.git"
    target_dir = r"D:\BaiduNetdiskDownload\ai_agent_with_langchain\.code\vue3-element-admin_test"
    
    # Clean up first
    if os.path.exists(target_dir):
        print(f"Cleaning up {target_dir}")
        run_shell_command(f'rmdir /s /q "{target_dir}"')

    print("Starting clone...")
    cmd = f'git clone --depth 1 --progress --verbose {repo_url} "{target_dir}"'
    result = run_shell_command(cmd)
    print("Clone finished.")
    print("Result:", result)

if __name__ == "__main__":
    test_clone()
