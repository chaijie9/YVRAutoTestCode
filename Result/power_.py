import subprocess
import datetime
import sys
import time

from dingtalkchatbot.chatbot import DingtalkChatbot

webhook = 'https://oapi.dingtalk.com/robot/send?access_token' \
          '=ac6710a1ccc6f62d22e0cd8aa690986f5cf3afb2064f60e63c7a4b832d64b622 '
ding = DingtalkChatbot(webhook)
def check_adb_device():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
        output = result.stdout
        if 'offline'  in output:
            return False
        else:
            return True
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        return False

if __name__ == '__main__':
    print("开始时间=====", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    while True:
        if not check_adb_device():
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("结束时间=====", current_time)
            ding.send_text(f"结束时间====={current_time}" , is_at_all=True)

            time.sleep(5)
            sys.exit()

            # 开始时间===== 2024-12-09 20:47:57

            # 开始时间===== 2024-12-11 20:45:21