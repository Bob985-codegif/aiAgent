import os
import subprocess


def test_git_clone():
    """直接测试git clone命令"""
    repo_url = "https://github.com/youlaitech/vue3-element-admin.git"
    # 使用原始字符串避免转义问题
    project_root = r"D:\BaiduNetdiskDownload\ai_agent_with_langchain"
    target_dir = os.path.join(project_root, ".code")
    repo_dir = os.path.join(target_dir, "vue3-element-admin")

    # 确保目标目录存在
    if not os.path.exists(target_dir):
        print(f"创建目录: {target_dir}")
        os.makedirs(target_dir)

    # 如果仓库目录已存在，先删除
    if os.path.exists(repo_dir):
        print(f"删除已存在的目录: {repo_dir}")
        import shutil
        shutil.rmtree(repo_dir)

    # 构建完整的克隆命令
    clone_cmd = f"git clone {repo_url} {repo_dir}"
    print(f"执行命令: {clone_cmd}")

    try:
        # 执行命令
        result = subprocess.run(
            clone_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60  # 设置超时时间
        )

        if result.returncode == 0:
            print("✅ 克隆成功!")
            print(f"输出: {result.stdout}")
            return True
        else:
            print(f"❌ 克隆失败，返回码: {result.returncode}")
            print(f"错误信息: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ 克隆超时")
        return False
    except Exception as e:
        print(f"❌ 克隆过程中发生异常: {str(e)}")
        return False


if __name__ == "__main__":
    test_git_clone()
