## 问题分析

运行 `code_agent.py` 时出现以下错误：

1. 路径处理问题：`SyntaxWarning: invalid escape sequence '\B'`
2. 路径被错误解析：`D:\\BaiduNetdiskDownload\x07i_agent_with_langchain\x07pp\\code_agent\\mcp\\mysql_tools.py`（注意 `\x07` 转义字符）
3. 最终导致连接关闭：`mcp.shared.exceptions.McpError: Connection closed`

## 根本原因

在 `app/code_agent/tools/mysql_tools.py` 中，路径拼接逻辑存在问题，导致生成的路径包含无效的转义序列，最终使 MCP 客户端无法正确找到和执行 MySQL 工具文件。

## 修复方案

### 1. 修复路径处理逻辑

修改 `app/code_agent/tools/mysql_tools.py` 文件：

* 确保路径拼接使用正确的方法

* 避免硬编码路径分隔符

* 确保生成的路径在传递给 MCP 客户端时是正确的

### 2. 关键修改点

```python
# 原代码（有问题）
project_root = os.path.dirname(os.path.dirname(current_dir))
mysql_tools_path = os.path.join(
    project_root,
    'app',
    'code_agent',
    'mcp',
    'mysql_tools.py'
)

# 修复后代码
# 直接使用绝对路径，避免多层嵌套的dirname调用
mysql_tools_path = os.path.abspath(
    os.path.join(
        current_dir,
        '..', '..',  # 回到project_root
        'app', 'code_agent', 'mcp', 'mysql_tools.py'
    )
)
```

### 3. 额外改进

* 添加更详细的路径调试信息

* 确保路径在打印和传递前都经过正确的规范化处理

* 检查并修复可能存在的其他路径处理问题

## 预期结果

修复后，`code_agent.py` 应该能够：

1. 正确生成 MySQL 工具文件的路径
2. 成功启动 MCP 客户端
3. 正常运行并接受用户输入
4. 能够使用 MySQL 工具执行数据库操作

## 后续测试

1. 运行 `python app/code_agent/agent/code_agent.py` 测试修复效果
2. 输入简单的 MySQL 相关命令，验证工具是否正常工作
3. 检查是否还有其他路径相关的错误

## 注意事项

* 修复时要确保代码兼容 Windows 和 Linux/macOS 系统

* 避免使用硬编码的路径分隔符

* 始终使用 `os.path` 模块处理路径

* 添加适当的错误

