@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title AI Vision Data and Training Workbench Preview

echo ================================================
echo AI Vision Data and Training Workbench Preview
echo 一键启动预览版界面
 echo ================================================
echo.
echo [1/3] 正在检查 Python...
where python >nul 2>nul
if errorlevel 1 (
    echo 未检测到 Python。
    echo 请先安装 Python 3.10，并确保 python 命令可用。
    echo.
    pause
    exit /b 1
)

echo [2/3] 正在检查项目文件...
if not exist "main.py" (
    echo 未找到 main.py。
    echo 请确认你是在项目根目录中运行此脚本。
    echo.
    pause
    exit /b 1
)

if not exist "logs" mkdir "logs"

echo [3/3] 正在启动工作台...
echo 首次启动如果较慢，属于正常现象。
echo 如果启动失败，请查看：
echo C:\AI_Workbench\logs\startup_error.log
echo.
python main.py
set ERR=%ERRORLEVEL%

echo.
if not "%ERR%"=="0" (
    echo 程序退出代码：%ERR%
    echo 启动可能失败了，请检查日志。
    pause
    exit /b %ERR%
)

echo 程序已退出。
endlocal
