import re
import subprocess
import time

# test_count = 1
# error = 0
# while True:
#     cj = input(" ")
#     if cj == "00":
#         error += 1
#         print("错误，退出")
#         break
#     else:
#         test_count += 1
#         print(test_count)
now_time = time.strftime("%H_%M_%S")
init_command = 'adb logcat -d | findstr "ready!!!!!!!!!"'
p_obj = subprocess.Popen(
    args=init_command,
    stdin=None, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, shell=True)
for line in p_obj.stdout:
    msg = str(line).replace("b'", "").replace(r"\r\n'", "").replace("'", "") \
        .replace("[", "").replace("]", "").replace(r"\t", "").replace(r"\n", '')
if msg.find("Low frequency vio state is delivered. 6DOF is ready!!!!!!") >= 0:
    # result = re.findall(r"6DOF is ready!!!!!!!!!", msg)
    print("初始化成功")

else:
    print("xx")
    # else:
    #     print("初始化失败")
    #     # subprocess.call(f"adb logcat -d > ./LOG/{now_time}.txt", shell=True)
    #     print("log OK")
    #     # time.sleep(3)


# subprocess.call("adb pull /system/build.prop ./tomb")
# subprocess.call("adb shell rm -rf /data/tombstones/")
# subprocess.call("adb shell rm -rf /data/tombstones/*", shell=True)
