# # import re
# #
# # filename = "./cj.txt"
# # with open(filename, "r",encoding='utf-8') as f:
# #     result_data = f.readlines()
# #     for eachline in result_data:
# #         if eachline.find(".cpp: FPS") >= 0:
# #             # print(eachline)
# #             # FpsCount += 1
# #             fps = re.findall("FPS=(.*?)/", eachline)[0]
# #             print(fps)
import subprocess
import time

# from time import time

from slamawake import adb_command
#
# if __name__ == '__main__':
#     def check_crash():
#         result_tomb = adb_command("adb -s D3HDXD2D4363000186  shell ls data/tombstones/")
#         result_anr = adb_command("adb -s D3HDXD2D4363000186  shell ls data/anr/")
#         now_time = time.strftime("%H_%M_%S")
#         if result_tomb.find("_") > 0 or result_anr.find("_") > 0:
#             subprocess.call(f"adb -s D3HDXD2D4363000186 logcat -d > ./LOG/crash_{now_time}_{test_count}次.txt",
#                             shell=True)
#             subprocess.call(f"adb -s D3HDXD2D4363000186  pull /data/tombstones  ./tomb/{now_time}")
#             time.sleep(2)
#             subprocess.call("adb -s D3HDXD2D4363000186  shell rm -rf /data/tombstones/*", shell=True)
#             subprocess.call("adb -s D3HDXD2D4363000186  shell rm -rf /data/anr/*", shell=True)
#             time.sleep(2)
#             return True
#         else:
#             return False
#
#
#     check_crash()

# def imu_init():
#     init_command = 'adb -s D3HDXD2D4363000186 logcat -d | findstr "HMDImuModule"'
#     p_obj = subprocess.Popen(
#         args=init_command,
#         stdin=None, stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE, shell=True)
#     for line in p_obj.stdout:
#         msg = str(line).replace("b'", "").replace(r"\r\n'", "").replace("'", "") \
#             .replace("[", "").replace("]", "").replace(r"\t", "").replace(r"\n", '')
#     if msg.find("Start imu main loop") >= 0:
#         # result = re.findall(r"6DOF is ready!!!!!!!!!")
#         print("IMU运行正常")
#         return True
#     else:
#         return False
#
#
# print(imu_init())

def check_adb_device():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
        output = result.stdout
        if '192.168.8.107:5555      device' in output:
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        print("异常1")
        return False
    except Exception as e:
        print("异常2")
        return False

sn = "192.168.8.107:5555"
connect = f"adb connect {sn}"
if __name__ == '__main__':


    while True:
        if not check_adb_device():
            print("weilianjie")
            subprocess.call(connect, shell=True)
            print("执行连接")
            time.sleep(2)
            continue
        else:
            print("lianjiela")

