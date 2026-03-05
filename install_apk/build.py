import PyInstaller.__main__

PyInstaller.__main__.run([
    'install_apk.py',  # 替换为你的脚本文件名
    '--onefile',
    '--name=DeviceAutomation',
    '--console',
    '--add-data=adb.exe;.',  # 如果需要包含adb可执行文件
    '--hidden-import=concurrent.futures.thread'
])