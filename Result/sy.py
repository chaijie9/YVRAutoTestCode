# import re
#
# from slamawake import adb_command
#
#
# def check_none_hand():
#     msg = adb_command("adb shell logcat -d | grep 'OnInputDeviceChanged' | tail -1")
#     result = re.findall(r"input device changed:(.*)", msg)
#     print(result)
#     return result
#
#
# print(check_none_hand())
import subprocess
import time

from dingtalkchatbot.chatbot import DingtalkChatbot

from slamawake import adb_command

# now_time = time.strftime("%H:%M:%S")
# webhook = 'https://oapi.dingtalk.com/robot/send?access_token' \
#           '=ac6710a1ccc6f62d22e0cd8aa690986f5cf3afb2064f60e63c7a4b832d64b622 '
# ding = DingtalkChatbot(webhook)
# test_count = 6
# while True:
#     subprocess.call("adb reboot") # off
#     print("adb reboot")
#     time.sleep(50)
#     print("start")
#     start_modeC = "adb shell am broadcast -a com.yvr.demo.action.dev.mode --include-stopped-packages"
#     print(start_modeC)
#     subprocess.call(start_modeC, shell=True, timeout=15)
#     time.sleep(3)
#     root = "adb wait-for-device shell setprop service.dev.mode 1"
#     print(root)
#     subprocess.call(root, shell=True, timeout=10)
#     time.sleep(5)
#     test_count += 1
#     print(f"第", {test_count}, "次")
#     result_tomb = adb_command("adb shell ls data/tombstones/")
#     result_anr = adb_command("adb shell ls data/anr/")
#     print(result_tomb, result_anr)
#     if result_tomb.find("_") > 0 or result_anr.find("_") > 0:
#         ding.send_text(time.strftime("%H:%M:%S") + f' 第 {test_count} 次重启后crash', is_at_all=False)
#     else:
#
#         print(f"第 {test_count} 次，当前无crash")
now_time = time.strftime("%H_%M_%S")

result_tomb = adb_command("adb shell ls data/tombstones/")
result_anr = adb_command("adb shell ls data/anr/")
print(result_tomb, result_anr)

if result_tomb.find("_") > 0 or result_anr.find("_") > 0:
    subprocess.call(f"adb logcat -d > ./LOG/crash_{now_time}_11.txt", shell=True)
    subprocess.call(f"adb pull /data/tombstones  ./tomb/crash_{now_time}_11/")