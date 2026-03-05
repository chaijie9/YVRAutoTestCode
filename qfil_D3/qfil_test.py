import subprocess
import os
import time
from dingtalkchatbot.chatbot import DingtalkChatbot

from slamawake import adb_command

webhook = 'https://oapi.dingtalk.com/robot/send?access_token' \
          '=ac6710a1ccc6f62d22e0cd8aa690986f5cf3afb2064f60e63c7a4b832d64b622 '
ding = DingtalkChatbot(webhook)

def reboot_to_edl():
    """
    使用 adb 切换设备到 EDL 模式。
    """
    try:
        print("正在重启设备到 EDL 模式...")
        subprocess.run(["adb", "reboot", "edl"], check=True)
        print("设备已进入 EDL 模式，等待设备识别...")
        time.sleep(3)  # 等待设备进入 EDL 模式
    except subprocess.CalledProcessError:
        print("ADB 命令失败，请确保设备已连接并启用调试模式。")
        exit(1)


def flash_with_qfil():
    """
    使用 QFIL 命令行进行固件烧录。

    :param qfil_path: QFIL 工具路径，例如 "C:/Program Files (x86)/Qualcomm/QPST/bin/QFIL.exe"
    :param firehose_file: Firehose 文件路径，例如 "prog_emmc_firehose_XXX.mbn"
    :param rawprogram_file: 分区映射文件，例如 "rawprogram0.xml"
    :param patch_file: 补丁文件，例如 "patch0.xml"
    :param com_port: 设备的 COM 端口号，例如 "COM3"
    """
    try:
        command = (r'"C:\Program Files (x86)\Qualcomm\QPST\bin\QFIL.exe" -COM=3 -Mode=3 -PROGRAMMER=True;"D:\D3_DEV_3.0.1.310_qfil\prog_firehose_ddr.elf" -SEARCHPATH="D:\D3_DEV_3.0.1.310_qfil" -RawProgram="D:\D3_DEV_3.0.1.310_qfil\rawprogram.xml" -patch="D:\D3_DEV_3.0.1.310_qfil\patch.xml" -RESETSAHARASTATEMACHINE=True -RESETAFTERDOWNLOAD=True -DOWNLOADFLAT')
        # 确保程序路径在引号中
        print("开始烧录")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,timeout=400)

        # if "Waiting for reset done..." in result:
        if result.stdout.find("Waiting for reset done...") > 0:
            print("烧录成功!")
            # print("输出信息:", result.stdout)
        else:
            print("烧录失败!")
            print("错误信息:", result.stderr)

    except Exception as e:
        print("出现异常:", str(e))


def head_init():
    init_command = 'adb logcat -d | findstr "delivered."'
    p_obj = subprocess.Popen(
        args=init_command,
        stdin=None, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell=True)
    for line in p_obj.stdout:
        msg = str(line).replace("b'", "").replace(r"\r\n'", "").replace("'", "") \
            .replace("[", "").replace("]", "").replace(r"\t", "").replace(r"\n", '')
    if msg.find("Low frequency vio state is delivered. 6DOF is ready!!!!!!") >= 0:
        # result = re.findall(r"6DOF is ready!!!!!!!!!")
        return print("初始化成功")
    else:
        return False
# qfil_executable_path = r"C:\Program Files (x86)\Qualcomm\QPST\bin\QFIL.exe"
# firehose_path = r"C:\Users\chaijie\Desktop\D3_2.0.2.8_D3_2.0.2.8_qfil\prog_firehose_ddr.elf"
# rawprogram_path = r"C:\Users\chaijie\Desktop\D3_2.0.2.8_D3_2.0.2.8_qfil\rawprogram.xml"
# patch_path = r"C:\Users\chaijie\Desktop\D3_2.0.2.8_D3_2.0.2.8_qfil\patch.xml"
# # com_port = "40"  # 确保设备已连接到正确的端口

def check_node():
    try:
        result = subprocess.run(['adb', 'shell', 'ls', '/sys/class/drm/card0-DSI-1/modes'],
                                capture_output=True, text=True, check=True)
        output = result.stdout
        return "No such file or directory" not in output
    except subprocess.CalledProcessError as e:
        output = e.stderr
        return "No such file or directory" not in output

def start_root():
    start_modeC = "adb  shell am broadcast -a com.yvr.demo.action.dev.mode --include-stopped-packages"
    print(start_modeC)
    subprocess.call(start_modeC, shell=True, timeout=15)
    time.sleep(3)
    root = "adb shell setprop service.dev.mode 1"
    print(root)
    subprocess.call(root, shell=True, timeout=10)
    time.sleep(5)

def imu_init():
    init_command = 'adb -s D3HDXD2D4363000186 logcat -d | findstr "HMDImuModule"'
    p_obj = subprocess.Popen(
        args=init_command,
        stdin=None, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell=True)
    for line in p_obj.stdout:
        msg = str(line).replace("b'", "").replace(r"\r\n'", "").replace("'", "") \
            .replace("[", "").replace("]", "").replace(r"\t", "").replace(r"\n", '')
    if msg.find("Start imu main loop") >= 0:
        # result = re.findall(r"6DOF is ready!!!!!!!!!")
        print("IMU运行正常")
        return True
    else:
        return False

def check_crash():
    result_tomb = adb_command("adb -s D3HDXD2D4363000186  shell ls data/tombstones/")
    result_anr = adb_command("adb -s D3HDXD2D4363000186  shell ls data/anr/")
    now_time = time.strftime("%H_%M_%S")
    if result_tomb.find("_") > 0 or result_anr.find("_") > 0:
        subprocess.call(f"adb -s D3HDXD2D4363000186 logcat -d > ./LOG/crash_{now_time}_{test_count}次.txt", shell=True)
        subprocess.call(f"adb -s D3HDXD2D4363000186  pull /data/tombstones  ./tomb/{now_time}")
        time.sleep(2)
        return True
    else:
        return False
        # ding.send_text(time.strftime("%H:%M:%S") + f' 第 {test_count} 次q后crash', is_at_all=False)



# while True:
#     # 切换到 EDL 模式
#     reboot_to_edl()
#     time.sleep(3)
#     test_count += 1
#     # 调用烧录函数
#     flash_with_qfil()
#     time.sleep(75)
#     print("开始检查6dof初始化情况")
#     result = head_init()
#     # print(head_init())
#     if result is False:
#         print(f"第{test_count}次刷机后6DOF无法运行")
#         break
#     print(f"当前运行{test_count}次，未复现问题")
#
#
#



if __name__ == '__main__':
    # 切换到 EDL 模式
    test_count = 197
    while True:
        reboot_to_edl()
        time.sleep(3)
        test_count += 1
        # 调用烧录函数
        flash_with_qfil()
        time.sleep(75)
        print("检查IMU是否运行")
        time.sleep(15)
        now_time = time.strftime("%H_%M_%S")
        if imu_init() is True:
            print(f"第{test_count}次，未复现IMU问题")
        else:
            print(f"第{test_count}次，复现IMU问题!!!")
            subprocess.call(f"adb -s D3HDXD2D4363000186 logcat -d > ./LOG/imu_{now_time}_{test_count}次.txt",
                            shell=True)
            ding.send_text(time.strftime("%H:%M:%S") + f' 第 {test_count} 次IMU未运行！', is_at_all=True)
        time.sleep(5)
        start_root()
        time.sleep(5)
        if check_crash() is not True:
            print(f"第{test_count}次，未crash")
        else:
            print(f"第{test_count}次，crash!!!")
            subprocess.call(f"adb -s D3HDXD2D4363000186 logcat -d > ./LOG/crash_{now_time}_{test_count}次.txt",
                            shell=True)
            ding.send_text(time.strftime("%H:%M:%S") + f' 第 {test_count} 次crash！', is_at_all=False)
        # # result = head_init()
        # # print(head_init())
        # if result is False:
        #     print(f"第{test_count}次刷机后6DOF无法运行")
        #     break
        # print(f"当前运行{test_count}次，未复现问题")