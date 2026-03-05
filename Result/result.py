# import datetime
#
# a = '14:53:42.096'
# b = '14:53:42.505'
#
# # 将字符串转换为 datetime 对象
# a_dt = datetime.datetime.strptime(a, '%H:%M:%S.%f')
# b_dt = datetime.datetime.strptime(b, '%H:%M:%S.%f')
#
# # 计算时间差
# time_diff = (b_dt - a_dt).total_seconds() * 1000  # 将秒转换为毫秒
# millimeters = int(time_diff * 1000)  # 将毫秒转换为毫米
#
# print('a 和 b 之间的时间差为:', millimeters)
# import re
#
# CPU_list = []
# filename = "./source_.txt"
# with open(filename, "r") as f:
#     result_data = f.readlines()
#     for eachline in result_data:
#         if eachline.find("CPU%=") >= 0:
#             fps = float(re.findall("CPU%=(.*),", eachline)[0])
#             CPU_list.append(fps)
#
# print(CPU_list)
#
import subprocess


def check_adb_device():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
        output = result.stdout
        # print(output)
        if 'device' not in output:
            return False
        else:
            return True
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        return False

if __name__ == '__main__':
    check_adb_device()
