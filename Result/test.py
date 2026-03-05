# # # # # # Updated data based on the latest file content provided by the user
# # # # # import pandas as pd
# # # # #
# # # # # data_v6 = {
# # # # #     "Camera Combination": [
# # # # #         "C0-C1", "C0-C2", "C0-C3", "C0-C5", "C0-C6", "C0-C7",
# # # # #         "C1-C2", "C1-C3", "C1-C4", "C1-C5", "C1-C6", "C1-C7",
# # # # #         "C2-C3", "C2-C4", "C2-C5", "C2-C6", "C2-C7", "C3-C4",
# # # # #         "C3-C6", "C3-C7", "C4-C5", "C4-C6", "C4-C7", "C5-C6",
# # # # #         "C5-C7", "C6-C7"
# # # # #     ],
# # # # #     "Old Version Ratio Err (%)": [
# # # # #         -0.904500, 0.133553, 0.262589, -2.498730, 11.054077, -0.145782,
# # # # #         -0.222844, -0.341119, 3.842168, -1.577997, 0.211287, -0.676157,
# # # # #         1.614410, -1.339541, 4.968291, -0.194952, 1.663563, -2.296406,
# # # # #         -0.186848, 9.646738, -2.751197, 6.146454, -3.298776, -3.712280,
# # # # #         1.839962, -0.955030
# # # # #     ]
# # # # # }
# # # # #
# # # # # # Create DataFrame
# # # # # df_v6 = pd.DataFrame(data_v6)
# # # # #
# # # # # # Save to Excel file
# # # # # file_path_v6 = r"C:\Users\chaijie\Desktop\test_cj\1201\camera_ratio_errors_comparison_v6.xlsx"
# # # # # df_v6.to_excel(file_path_v6, index=False)
# # # # #
# # # # # file_path_v6
# # # #
# # # #
# # # #
# # # # # import subprocess
# # # # # import time
# # # # #
# # # # # while True:
# # # # #     output = subprocess.getoutput("adb shell dumpsys meminfo")
# # # # #     with open("memory_usage_log.txt", "a") as log_file:
# # # # #         log_file.write(f"Timestamp: {time.time()}\n")
# # # # #         log_file.write(output + "\n\n")
# # # # #     time.sleep(5)  # 每 60 秒采集一次
# # # #
# # # #
# # # #
# # # #
# # # # # import subprocess
# # # # # import time
# # # # # import re
# # # # # import matplotlib.pyplot as plt
# # # # #
# # # # # # 定义全局变量
# # # # # process_name = "trackingservice"  # 替换为目标进程名
# # # # # log_file_path = "memory_usage_log.txt"
# # # # # interval = 5  # 采样间隔，单位：秒
# # # # #
# # # # # # 数据存储
# # # # # timestamps = []
# # # # # memory_data = []
# # # # #
# # # # # def get_process_memory_info(process_name):
# # # # #     """
# # # # #     获取指定进程的 PSS、RSS、SwapPSS 数据
# # # # #     """
# # # # #     output = subprocess.getoutput("adb shell dumpsys meminfo")
# # # # #     process_pattern = re.compile(
# # # # #         rf"(\d+)\s+K:\s+{re.escape(process_name)}", re.MULTILINE
# # # # #     )
# # # # #     match = process_pattern.search(output)
# # # # #     if match:
# # # # #         memory_kb = int(match.group(1))
# # # # #         return memory_kb
# # # # #     return None
# # # # #
# # # # # def log_memory_data(process_name, log_file_path):
# # # # #     """
# # # # #     记录内存数据到日志文件
# # # # #     """
# # # # #     memory_kb = get_process_memory_info(process_name)
# # # # #     timestamp = time.time()
# # # # #     if memory_kb is not None:
# # # # #         with open(log_file_path, "a") as log_file:
# # # # #             log_file.write(f"{timestamp},{memory_kb}\n")
# # # # #         return timestamp, memory_kb
# # # # #     else:
# # # # #         print(f"Process '{process_name}' not found.")
# # # # #         return timestamp, None
# # # # #
# # # # # def plot_memory_trend(timestamps, memory_data, process_name):
# # # # #     """
# # # # #     绘制内存使用趋势图
# # # # #     """
# # # # #     plt.figure(figsize=(10, 6))
# # # # #     plt.plot(timestamps, memory_data, marker="o", linestyle="-", label="Memory (KB)")
# # # # #     plt.title(f"Memory Usage Trend for {process_name}")
# # # # #     plt.xlabel("Time")
# # # # #     plt.ylabel("Memory (KB)")
# # # # #     plt.legend()
# # # # #     plt.grid()
# # # # #     plt.xticks(rotation=45)
# # # # #     plt.tight_layout()
# # # # #     plt.show()
# # # # #
# # # # # def main():
# # # # #     print("Starting memory monitoring...")
# # # # #     try:
# # # # #         while True:
# # # # #             timestamp, memory_kb = log_memory_data(process_name, log_file_path)
# # # # #             if memory_kb is not None:
# # # # #                 print(f"[{time.ctime(timestamp)}] {process_name}: {memory_kb} KB")
# # # # #                 timestamps.append(time.ctime(timestamp))
# # # # #                 memory_data.append(memory_kb)
# # # # #             time.sleep(interval)
# # # # #     except KeyboardInterrupt:
# # # # #         print("\nMonitoring stopped. Generating memory trend plot...")
# # # # #         if timestamps and memory_data:
# # # # #             plot_memory_trend(timestamps, memory_data, process_name)
# # # # #         else:
# # # # #             print("No data to plot.")
# # # # #
# # # # # if __name__ == "__main__":
# # # # #     main()
# # # #     # def list_all_processes():
# # # #     #     """
# # # #     #     列出 dumpsys meminfo 输出中的所有进程
# # # #     #     """
# # # #     #     output = subprocess.getoutput("adb shell dumpsys meminfo")
# # # #     #     process_lines = [line for line in output.splitlines() if re.search(r'\d+K:\s', line)]
# # # #     #     print("Processes found in dumpsys meminfo:")
# # # #     #     for line in process_lines:
# # # #     #         print(line)
# # # #     #
# # # #     #
# # # #     # if __name__ == "__main__":
# # # #     #     list_all_processes()
# # # #
# # # #
# # # #
# # # # import os
# # # # import re
# # # # import time
# # # # import matplotlib.pyplot as plt
# # # # from datetime import datetime
# # # # import subprocess
# # # #
# # # # # # 配置参数
# # # # # PROCESS_NAME = "trackingservice"  # 目标进程名称
# # # # # INTERVAL = 5  # 采样间隔时间，单位：秒
# # # # # DURATION = 20  # 总监控时长，单位：秒
# # # # # OUTPUT_FILE = "memory_log.txt"  # 记录文件路径
# # # # #
# # # # #
# # # # #
# # # # #     """
# # # # #     从 dumpsys meminfo 中获取目标进程的内存信息。
# # # # #     :param process_name: 要监控的进程名称
# # # # #     :return: (timestamp, pss, rss) 元组
# # # # #     """
# # # # #     output = subprocess.getoutput("adb shell dumpsys meminfo")
# # # # #     match = re.search(rf"(\d+,?\d+)K:\s+{process_name}.*", output)
# # # # #     if match:
# # # # #         memory_rss = int(match.group(1).replace(",", ""))  # 解析内存值，单位 KB
# # # # #         timestamp = datetime.now().strftime("%H:%M:%S")
# # # # #         return timestamp, memory_rss
# # # # #     return None
# # # # #
# # # # #
# # # # # def log_memory_usage(process_name, duration, interval, output_file):
# # # # #     """
# # # # #     周期性记录目标进程的内存信息到文件中。
# # # # #     :param process_name: 要监控的进程名称
# # # # #     :param duration: 总监控时间，单位：秒
# # # # #     :param interval: 采样间隔，单位：秒
# # # # #     :param output_file: 输出日志文件
# # # # #     """
# # # # #     end_time = time.time() + duration
# # # # #     with open(output_file, "w") as f:
# # # # #         f.write("Timestamp, RSS (KB)\n")
# # # # #         while time.time() < end_time:
# # # # #             meminfo = get_meminfo(process_name)
# # # # #             if meminfo:
# # # # #                 f.write(f"{meminfo[0]}, {meminfo[1]}\n")
# # # # #                 print(f"[{meminfo[0]}] {process_name} RSS: {meminfo[1]} KB")
# # # # #             else:
# # # # #                 print(f"[{datetime.now().strftime('%H:%M:%S')}] Process '{process_name}' not found.")
# # # # #             time.sleep(interval)
# # # # #
# # # # #
# # # # # def plot_memory_usage(file_path):
# # # # #     """
# # # # #     从日志文件中读取内存信息并绘制内存使用趋势图。
# # # # #     :param file_path: 内存日志文件路径
# # # # #     """
# # # # #     timestamps, memory_rss = [], []
# # # # #     with open(file_path, "r") as f:
# # # # #         next(f)  # 跳过表头
# # # # #         for line in f:
# # # # #             timestamp, rss = line.strip().split(", ")
# # # # #             timestamps.append(timestamp)
# # # # #             memory_rss.append(int(rss))
# # # # #
# # # # #     plt.figure(figsize=(10, 6))
# # # # #     plt.plot(timestamps, memory_rss, marker='o', label="RSS (KB)")
# # # # #     plt.xlabel("Time")
# # # # #     plt.ylabel("Memory Usage (KB)")
# # # # #     plt.title(f"Memory Usage for Process: {PROCESS_NAME}")
# # # # #     plt.xticks(rotation=45)
# # # # #     plt.grid(True)
# # # # #     plt.legend()
# # # # #     plt.tight_layout()
# # # # #     plt.show()
# # # # #
# # # # #
# # # # # if __name__ == "__main__":
# # # # #     print("Starting memory monitoring...")
# # # # #     log_memory_usage(PROCESS_NAME, DURATION, INTERVAL, OUTPUT_FILE)
# # # # #     print(f"Memory log saved to {OUTPUT_FILE}.")
# # # # #     plot_memory_usage(OUTPUT_FILE)
# # # #
# # # # def check_adb_device():
# # # #     try:
# # # #         result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
# # # #         output = result.stdout
# # # #         if '192.168.8.126:5555	device' in output:
# # # #             return False
# # # #         else:
# # # #             return True
# # # #     except subprocess.TimeoutExpired:
# # # #         return False
# # # #     except Exception as e:
# # # #         return False
# # # #
# # # # connect = "adb connect 192.168.8.126:5555"
# # # # # while True:
# # # #
# # # # if not check_adb_device():
# # # #     print("连接")
# # # # else:
# # # #     print("未连接")
# # # #
# # # #
# # # # # result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
# # # # # output = result.stdout
# # # # # print(output)
# # #
# # # import os
# # # import re
# # # import subprocess
# # # import time
# # #
# # # import openpyxl
# # # from dingtalkchatbot.chatbot import DingtalkChatbot
# # # from slamawake import adb_command
# # # def check_adb_device():
# # #     try:
# # #         result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
# # #         output = result.stdout
# # #         if '192.168.8.107:5555	device' in output:
# # #             return False
# # #         else:
# # #             return True
# # #     except subprocess.TimeoutExpired:
# # #         return False
# # #     except Exception as e:
# # #         return False
# # #
# # #
# # # now_time = time.strftime("%H_%M_%S")
# # # webhook = 'https://oapi.dingtalk.com/robot/send?access_token' \
# # #           '=ac6710a1ccc6f62d22e0cd8aa690986f5cf3afb2064f60e63c7a4b832d64b622 '
# # # ding = DingtalkChatbot(webhook)
# # # Excel_File = r"./reboot_D3_RC_D3.0.1.44+resAlg.xlsx"
# # # if not os.path.exists(Excel_File):
# # #     wb = openpyxl.Workbook()
# # #     wb.create_sheet(title=str("Slam_Log_MSG"), index=0)
# # #     wb.save(Excel_File)
# # # workbook1 = openpyxl.load_workbook(Excel_File)
# # # sh = workbook1["Slam_Log_MSG"]
# # # ItemIndex = ["测试次数", "初始化是否成功", "mapping重定位成功", "crash" ]
# # # count = 1
# # # for Item in ItemIndex:
# # #     sh.cell(1, count, value=Item)
# # #     count = count + 1
# # # workbook1.save(Excel_File)
# # # test_count =115
# # # error = 0
# # # connect = "adb connect 192.168.8.107:5555"
# # # sn = " -s 192.168.8.107:5555"
# # #
# # # while True:
# # #     while True:
# # #         if check_adb_device():
# # #             subprocess.call(connect)
# # #             time.sleep(5)
# # #         else:
# # #             subprocess.call(f"adb {sn} reboot ")
# # #             sh.cell(1 + test_count, 1, value=test_count)
# # #             # subprocess.call("adb -s D3HDXD2D4363000102  shell input keyevent 223") # off
# # #             time.sleep(55)
# # #             # subprocess.call("adb -s D3HDXD2D4363000186 shell am start -n com.oculus.sdk.yvrmesh/com.oculus.NativeActivity")
# # #             # print("开MESH")
# # #             start_modeC = f"adb {sn} shell am broadcast -a com.yvr.demo.action.dev.mode --include-stopped-packages"
# # #             print(start_modeC)
# # #             subprocess.call(start_modeC, shell=True, timeout=15)
# # #             time.sleep(3)
# # #             root = f"adb {sn}  shell setprop service.dev.mode 1"
# # #             print(root)
# # #             subprocess.call(root, shell=True, timeout=10)
# # #             time.sleep(5)
# # #             # subprocess.call("adb -s D3HDXD2D4363000102 shell input keyevent 224") # on
# # #             print("start")
# # #             time.sleep(8)
# # #             init_command = f'adb {sn}   logcat -d | findstr "delivered."'
# # #             p_obj = subprocess.Popen(
# # #                 args=init_command,
# # #                 stdin=None, stdout=subprocess.PIPE,
# # #                 stderr=subprocess.PIPE, shell=True)
# # #             for line in p_obj.stdout:
# # #                 msg = str(line).replace("b'", "").replace(r"\r\n'", "").replace("'", "") \
# # #                     .replace("[", "").replace("]", "").replace(r"\t", "").replace(r"\n", '')
# # #             if msg.find("Low frequency vio state is delivered. 6DOF is ready!!!!!!") >= 0:
# # #                 # result = re.findall(r"6DOF is ready!!!!!!!!!")
# # #                 sh.cell(1 + test_count, 2, value="PASS")
# # #                 print("初始化成功")
# # #             else:
# # #                 sh.cell(1 + test_count, 2, value="FAIL")
# # #                 now_time = time.strftime("%H_%M_%S")
# # #                 subprocess.call(f"adb {sn} logcat -d > ./LOG/no_init_{now_time}_{test_count}次.txt", shell=True)
# # #                 ding.send_text(time.strftime("%H:%M:%S") + f' 第 {test_count} 次重启后初始化失败', is_at_all=False)
# # #                 print("初始化失败")
# # #                 time.sleep(2)
# # #
# # #             # recenter_command = 'adb -s D3HDXD2D4363000186 logcat -d | findstr "large_space_map_recognized"'
# # #             # p_obj = subprocess.Popen(
# # #             #     args=recenter_command,
# # #             #     stdin=None, stdout=subprocess.PIPE,
# # #             #     stderr=subprocess.PIPE, shell=True)
# # #             # for line in p_obj.stdout:
# # #             #     msg = str(line).replace("b'", "").replace(r"\r\n'", "").replace("'", "") \
# # #             #         .replace("[", "").replace("]", "").replace(r"\t", "").replace(r"\n", '')
# # #             # if msg.find("large_space_map_recognized setRecenterPose") >= 0:
# # #             #     sh.cell(1 + test_count, 3, value="PASS")
# # #             #     print("mapping 重定位成功")
# # #             # else:
# # #             #     sh.cell(1 + test_count, 3, value="FAIL")
# # #             #     print("mapping 重定位失败")
# # #             #     time.sleep(2)
# # #             #     subprocess.call(f"adb -s D3HDXD2D4363000186  logcat -d > ./LOG/{now_time}_{test_count}次.txt", shell=True)
# # #             # time.sleep(3)
# # #             # subprocess.call("adb shell dumpsys vrruntimeservice_native --do_recenter")
# # #
# # #             recenter_command = f'adb {sn} logcat -d | findstr "Merge"'
# # #             p_obj = subprocess.Popen(
# # #                 args=recenter_command,
# # #                 stdin=None, stdout=subprocess.PIPE,
# # #                 stderr=subprocess.PIPE, shell=True)
# # #             for line in p_obj.stdout:
# # #                 msg = str(line).replace("b'", "").replace(r"\r\n'", "").replace("'", "") \
# # #                     .replace("[", "").replace("]", "").replace(r"\t", "").replace(r"\n", '')
# # #             time.sleep(5)
# # #             msg = adb_command(recenter_command)
# # #             if msg.find("mapping Merge global map") >= 0:
# # #                 sh.cell(1 + test_count, 3, value="PASS")
# # #                 print("mapping 重定位成功")
# # #             else:
# # #                 sh.cell(1 + test_count, 3, value="FAIL")
# # #                 print("mapping 重定位失败")
# # #                 time.sleep(2)
# # #                 now_time = time.strftime("%H_%M_%S")
# # #                 # subprocess.call(f"adb -s 192.168.8.115:5555 logcat -d > ./LOG/{now_time}_{test_count}.txt", shell=True)
# # #                 # subprocess.call(f"adb -s D3HDXD2D4363000186 logcat -d > ./LOG/{now_time}_{test_count}.txt", shell=True)
# # #
# # #             print(f"第", test_count, "次")
# # #             result_tomb = adb_command(f"adb {sn}  shell ls data/tombstones/")
# # #             result_anr = adb_command(f"adb {sn}  shell ls data/anr/")
# # #             print(result_tomb, result_anr)
# # #
# # #
# # #             if result_tomb.find("_") > 0 or result_anr.find("_") > 0:
# # #                 now_time = time.strftime("%H_%M_%S")
# # #                 subprocess.call(f"adb {sn} logcat -d > ./LOG/crash_{now_time}_{test_count}次.txt", shell=True)
# # #                 subprocess.call(f"adb {sn}  pull /data/tombstones  ./tomb/{now_time}")
# # #                 time.sleep(2)
# # #                 subprocess.call(f"adb {sn}  shell rm -rf /data/tombstones/*", shell=True)
# # #                 subprocess.call(f"adb {sn}  shell rm -rf /data/anr/*", shell=True)
# # #                 time.sleep(2)
# # #                 ding.send_text(time.strftime("%H:%M:%S") + f' 第 {test_count} 次重启后crash', is_at_all=False)
# # #             else:
# # #                 sh.cell(1 + test_count, 4, value="NO")
# # #                 print(f"第 {test_count} 次，当前无crash")
# # #             test_count += 1
# # #             workbook1.save(Excel_File)
# # # workbook1.save(Excel_File)
# # #
# # #
# # #
# # #
# # #
# # #
# # import pandas as pd
# # import numpy as np
# # import matplotlib.pyplot as plt  # 可选：用于可视化趋势
# #
# # # 读取并解析数据（修复Frame解析问题）
# # data = []
# # with open(output_假眼.txt", "r") as f:
# #     for line in f:r"C:\Users\124512\Desktop\EyeTest\
# #         line = line.strip()
# #         if not line or ":" not in line:  # 跳过无效行
# #             continue
# #         parts = line.split()
# #         frame_part = parts[1].rstrip(':')  # 提取Frame编号并去除冒号
# #         x = float(parts[2])
# #         y = float(parts[3])
# #         data.append({"Frame": int(frame_part), "X": x, "Y": y})
# #
# # df = pd.DataFrame(data)
# #
# # # 计算全局总体统计量
# # global_stats = {
# #     "X_std": df["X"].std(ddof=0),
# #     "X_var": df["X"].var(ddof=0),
# #     "Y_std": df["Y"].std(ddof=0),
# #     "Y_var": df["Y"].var(ddof=0)
# # }
# #
# # # 选择稳定阶段（示例：去除首尾1000帧）
# # if len(df) > 2000:
# #     stable_df = df.iloc[1000:-1000].copy()
# #     stable_stats = {
# #         "X_std": stable_df["X"].std(ddof=0),
# #         "X_var": stable_df["X"].var(ddof=0),
# #         "Y_std": stable_df["Y"].std(ddof=0),
# #         "Y_var": stable_df["Y"].var(ddof=0)
# #     }
# # else:
# #     stable_stats = None
# #     print("数据长度不足，无法提取中间稳定段")
# #
# # # 打印结果（可选：可视化趋势）
# # print("全局统计量：", global_stats)
# # if stable_stats:
# #     print("稳定阶段统计量：", stable_stats)
# #
# # # 可视化趋势（查看X/Y的波动情况）
# # plt.figure(figsize=(12, 6))
# # plt.subplot(2, 1, 1)
# # plt.plot(df["Frame"], df["X"], label="X")
# # plt.title("X Value Trend")
# # plt.subplot(2, 1, 2)
# # plt.plot(df["Frame"], df["Y"], label="Y", color="red")
# # plt.title("Y Value Trend")
# # plt.tight_layout()
# # plt.show()
#
#
# import pandas as pd
# import numpy as np
#
# # 读取数据并解析
# data = []
# with open(r"C:\Users\124512\Desktop\EyeTest\output_新真眼.txt", "r") as f:
#     for line in f:
#         line = line.strip()
#         if not line or ":" not in line:
#             continue
#         parts = line.split()
#         frame = int(parts[1].rstrip(':'))  # 去除冒号并转换为整数
#         x = float(parts[2])
#         y = float(parts[3])
#         data.append({"Frame": frame, "X": x, "Y": y})
#
# df = pd.DataFrame(data)
# print(f"数据总行数: {len(df)}")  # 输出：数据总行数: 22987（实际行数以文件为准）
#
# # 全局统计量（ddof=0表示总体统计量）
# global_stats = {
#     "X_std": df["X"].std(ddof=1),
#     "X_var": df["X"].var(ddof=1),
#     "Y_std": df["Y"].std(ddof=1),
#     "Y_var": df["Y"].var(ddof=1)
# }
#
# print("全局统计量：")
# for key, value in global_stats.items():
#     print(f"{key}: {value:.6f}")
#
# # 计算中间500帧的索引（总长度需大于500）
# total_length = len(df)
# if total_length > 500:
#     mid_start = total_length // 2 - 250
#     mid_end = total_length // 2 + 250
#     stable_df = df.iloc[mid_start:mid_end].copy()
#
#     stable_stats = {
#         "X_std": stable_df["X"].std(ddof=1),
#         "X_var": stable_df["X"].var(ddof=1),
#         "Y_std": stable_df["Y"].std(ddof=1),
#         "Y_var": stable_df["Y"].var(ddof=1)
#     }
#
#     print("\n中间500帧统计量：")
#     for key, value in stable_stats.items():
#         print(f"{key}: {value:.6f}")
# else:
#     print("数据不足500帧，无法提取中间段。")

import numpy as np

# 解析数据（示例代码）
frames = []
with open(r"C:\Users\124512\Desktop\EyeTest\output_无滤波真眼.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        var1 = float(parts[2])
        var2 = float(parts[3])
        frames.append((var1, var2))

# 转换为数组
var1_global = np.array([x[0] for x in frames])
var2_global = np.array([x[1] for x in frames])

# 计算全局统计量
std_var1_global = np.std(var1_global,ddof=1)
var_var1_global = np.var(var1_global,ddof=1)
std_var2_global = np.std(var2_global,ddof=1)
var_var2_global = np.var(var2_global,ddof=1)

print("max  ",np.max(var2_global))
print("min  ", np.min(var2_global))
print("avg  ", np.mean(var2_global))
# print(sum(var1_global)/len(var1_global))
# for n in var1_global:
#     if n >=0:
#         print(n)


# 提取中间500帧
n = len(frames)
start = n//2 - 250
end = start + 500
var1_stable = var1_global[start:end]
var2_stable = var2_global[start:end]

# 计算稳定阶段统计量
std_var1_stable = np.std(var1_stable)
var_var1_stable = np.var(var1_stable)
std_var2_stable = np.std(var2_stable)
var_var2_stable = np.var(var2_stable)

print("全局统计：")
print(f"变量1 - 标准差: {std_var1_global:.4f}, 方差: {var_var1_global:.7f}")
print(f"变量2 - 标准差: {std_var2_global:.4f}, 方差: {var_var2_global:.7f}\n")

print("稳定阶段统计：")
print(f"变量1 - 标准差: {std_var1_stable:.4f}, 方差: {var_var1_stable:.7f}")
print(f"变量2 - 标准差: {std_var2_stable:.4f}, 方差: {var_var2_stable:.7f}")