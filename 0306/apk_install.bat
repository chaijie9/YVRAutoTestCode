@echo off
chcp 65001 > nul 
REM set apk path
set APK_PATH=D:\cmd_\106_ad6fe1a3b9942fc6ed3dd4e139b3b3de.apk
for /f "tokens=1" %%i in ('.\adb devices ^| findstr /i "device$"') do (
    echo 正在安装APK到设备: %%i
    .\adb -s %%i install -r "%APK_PATH%"
    if errorlevel 1 (
        echo [错误] 安装到设备 %%i 失败
    ) else (
        echo [成功] 安装到设备 %%i 完成
    )
)

echo 所有设备安装完成
pause