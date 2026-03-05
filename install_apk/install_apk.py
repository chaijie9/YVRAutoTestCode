# -*- coding: utf-8 -*-
import subprocess
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
import os


def run_adb_command(device_id, command):
    """执行ADB命令并返回结果"""
    cmd = f"adb -s {device_id} {command}"
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"设备 {device_id} 执行失败: {e}")
        return None


def process_device(device_id, args):
    """处理单个设备的完整流程"""
    print(f"\n正在处理设备: {device_id}")

    # 1. 安装APK
    print("安装APK...")
    install_cmd = f"install -r {args.apk_path}"
    if run_adb_command(device_id, install_cmd):
        print("安装成功")
    else:
        print("安装失败")
        return

    # 2. 启动应用
    print("启动应用...")
    screen_on = f"shell input keyevent 224"
    run_adb_command(device_id, screen_on)
    launch_cmd = f"shell am start -n {args.package_name}/.{args.main_activity}"
    if run_adb_command(device_id, launch_cmd):
        print("启动成功")
    else:
        print("启动失败")

    # 3. 等待并退出
    # print(f"等待 {args.wait_time} 秒...")
    # time.sleep(args.wait_time)
    # print("关闭应用...")
    # stop_cmd = f"shell am force-stop {args.package_name}"
    # run_adb_command(device_id, stop_cmd)

    # 4. 复制文件夹
    print("复制文件...")
    if os.path.exists(args.source_folder):
        push_cmd = f"push {args.source_folder} {args.target_path}"
        if run_adb_command(device_id, push_cmd):
            print("文件复制成功")
        else:
            print("文件复制失败")
    else:
        print("源文件夹不存在")


def get_connected_devices():
    """获取已连接的设备列表"""
    result = subprocess.run(
        "adb devices",
        shell=True,
        capture_output=True,
        text=True
    )
    devices = [
        line.split()[0]
        for line in result.stdout.splitlines()
        if '\tdevice' in line
    ]
    return devices


def main():
    parser = argparse.ArgumentParser(description='多设备自动化处理脚本')
    parser.add_argument('--apk_path', required=True, help='APK文件路径')
    parser.add_argument('--package_name', required=True, help='应用包名')
    parser.add_argument('--main_activity', required=True, help='主Activity名称')
    parser.add_argument('--source_folder', required=True, help='源文件夹路径')
    parser.add_argument('--target_path', required=True, help='头显目标路径')
    parser.add_argument('--wait_time', type=int, default=5, help='等待时间（秒）')
    parser.add_argument('--max_workers', type=int, default=5, help='最大并发数')

    args = parser.parse_args()

    devices = get_connected_devices()
    if not devices:
        print("未检测到已连接的设备")
        return

    print(f"检测到 {len(devices)} 台设备: {', '.join(devices)}")

    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        for device in devices:
            executor.submit(process_device, device, args)


if __name__ == "__main__":
    main()
    # '''
    # python.exe .\0306\install_apk.py --apk_path C:\Users\124512\Documents\xhs.apk --package_name com.xingin.xhs --main_activity index.v2.IndexActivityV2  --source_folder C:\Users\124512\Documents\push_fuxi_v1.2.exe --target_path /sdcard/ --wait_time 5
    # '''