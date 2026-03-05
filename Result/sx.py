import os
import json
# 获取当前工作目录
import os
import subprocess
import time

from dingtalkchatbot.chatbot import DingtalkChatbot

test_count = 0
while True:
# 获取进程 PID
    process_pid = None
    for line in os.popen('adb shell ps -A | findstr trackingservice').readlines():
        process_name = line.split()[-1]
        if process_name == 'trackingservice':
            process_pid = int(line.split()[1])
            print(process_pid)
            break
    # 杀掉进程
    if process_pid == 5449:
        subprocess.call("adb shell input keyevent POWER")
    else:
        webhook = 'https://oapi.dingtalk.com/robot/send?access_token=ac6710a1ccc6f62d22e0cd8aa690986f5cf3afb2064f60e63c7a4b832d64b622'
        ding = DingtalkChatbot(webhook)
        ding.send_text(msg="watch_dog", is_at_all=False)
    #     subprocess.call(f'adb shell kill {process_pid}', shell=True)
    # test_count += 1
    # print(f"当前已手动kill trackingservice {test_count} 次")
    # time.sleep(10)
