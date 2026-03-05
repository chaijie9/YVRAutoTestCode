import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import subprocess
import threading

# ADB命令
adb_command_pid = 'adb shell "ps -A | grep com.yvr.home"'
adb_command_logcat = 'adb shell "logcat -t 1000 --pid=%PID% | grep PhaseCompleteFrame"'
adb_command_vrruntime = 'adb shell dumpsys vrruntimeservice_native -l 0x00040000'

# 使用正则表达式提取数据
pattern = r"\[(.*?)\]"  # 匹配方括号内的内容

# 初始化数据队列
max_data_points = 1000  # 最大数据点数
data_queue = deque(maxlen=max_data_points)

# 创建图表和子图
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

# 创建线图对象
line1, = ax1.plot([], [], 'b', label='Line Plot 1')
line2, = ax2.plot([], [], 'r', label='Line Plot 2')

# 绘制第一个y轴的数据（左侧）
ax1.set_xlabel('X-axis')
ax1.set_ylabel('Y-axis 1', color='b')
ax1.tick_params('y', colors='b')

# 绘制第二个y轴的数据（右侧）
ax2.set_ylabel('Y-axis 2', color='r')
ax2.tick_params('y', colors='r')

# 添加图例
lines = [line1, line2]
ax1.legend(lines, [line.get_label() for line in lines])

# 设置标题
plt.title('Line Plot')

# 数据可用标志
data_available = threading.Event()


def read_logcat():
    while True:
        # 打开开关
        dumpprocess = subprocess.Popen(adb_command_vrruntime, shell=True, stdout=subprocess.PIPE)
        dumpoutput = dumpprocess.stdout.read().decode('utf-8')

        # 获取进程ID
        process = subprocess.Popen(adb_command_pid, shell=True, stdout=subprocess.PIPE)
        output = process.stdout.read().decode('utf-8')
        pid = output.split()[1]

        # 通过ADB Shell获取日志数据
        adb_command_logcat_pid = adb_command_logcat.replace('%PID%', pid)
        logcat_process = subprocess.Popen(adb_command_logcat_pid, shell=True, stdout=subprocess.PIPE)
        logcat_output = logcat_process.stdout.read().decode('utf-8')

        # 提取数据
        lines = logcat_output.split('\n')
        for line in lines:
            matches = re.findall(pattern, line)
            if len(matches) >= 5:
                x_value = float(matches[0])
                y1_value = float(matches[1])
                y2_value = float(matches[2])
                data_queue.append((x_value, y1_value, y2_value))

        # 设置数据可用标志
        data_available.set()


def update_data(i):
    # 等待数据可用
    data_available.wait()

    # 清除数据可用标志
    data_available.clear()

    # 更新折线图数据
    x_data, y1_data, y2_data = zip(*data_queue)
    line1.set_data(x_data, y1_data)
    line2.set_data(x_data, y2_data)

    # 设置坐标轴范围
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()

    # 设置y轴的范围（保持一致）
    y_min = min(min(y1_data), min(y2_data))
    y_max = max(max(y1_data), max(y2_data))
    ax1.set_ylim(y_min, y_max)
    ax2.set_ylim(y_min, y_max)
    ax1.set_xlim(min(x_data), max(x_data))


# 创建动画
ani = FuncAnimation(fig, update_data, interval=1000)  # 每隔1秒更新数据

# 创建并启动子线程
logcat_thread = threading.Thread(target=read_logcat)
logcat_thread.start()

# 显示图表
plt.show()

# 等待子线程执行完毕
logcat_thread.join()
