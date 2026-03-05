import subprocess
import time
from dingtalkchatbot.chatbot import DingtalkChatbot

webhook = 'https://oapi.dingtalk.com/robot/send?access_token' \
          '=ac6710a1ccc6f62d22e0cd8aa690986f5cf3afb2064f60e63c7a4b832d64b622 '
ding = DingtalkChatbot(webhook)


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
    start_modeC = ("adb  shell am broadcast -a com.yvr.demo.action.dev.mode"
                   " --include-stopped-packages")
    print(start_modeC)
    subprocess.call(start_modeC, shell=True, timeout=15)
    time.sleep(3)
    root = "adb shell setprop service.dev.mode 1"
    print(root)
    subprocess.call(root, shell=True, timeout=10)
    time.sleep(5)


if __name__ == '__main__':
    test_count = 1
    while True:
        subprocess.call("adb reboot")
        test_count += 1
        time.sleep(55)
        start_root()
        if check_node() is True:
            print(f"第{test_count}次，未复现")
        else:
            print(f"第{test_count}次，复现!!!")
            ding.send_text(time.strftime("%H:%M:%S") + f' 第 {test_count} 次重启后节点异常', is_at_all=True)
            break