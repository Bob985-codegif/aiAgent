import os
from langchain_community.agent_toolkits.file_management import FileManagementToolkit
from langchain_community.tools import ShellTool

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
# 设置工作目录为项目根目录，以便能访问 .code 和 .workspace
root_dir = project_root
# 创建.code目录（如果不存在）
code_dir = os.path.join(project_root, ".code")
if not os.path.exists(code_dir):
    os.makedirs(code_dir)

file_tools = FileManagementToolkit(root_dir=root_dir).get_tools()

# 配置ShellTool，允许执行git命令
shell_tools = [ShellTool()]
