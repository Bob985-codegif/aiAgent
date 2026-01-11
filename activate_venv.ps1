# 简单的虚拟环境激活脚本

# 设置环境变量
$VIRTUAL_ENV = "$PSScriptRoot\.venv"
$PYTHONHOME = ""

# 添加虚拟环境Scripts目录到PATH
$Env:PATH = "$VIRTUAL_ENV\Scripts;$Env:PATH"

# 设置提示符前缀
function global:prompt {
    "(.venv) $(Get-Location) $ "
}

Write-Host "虚拟环境已激活: $VIRTUAL_ENV"
Write-Host "Python 可执行文件: $VIRTUAL_ENV\Scripts\python.exe"