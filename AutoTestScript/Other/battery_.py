# -*- coding: utf-8 -*-
import re
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 读取日志文件内容
with open(r'C:\Users\124512\Desktop\电量\D2HP132483D9000530_20250712_174658_第二次测试_cj\aa.txt', 'r', encoding='utf-8') as file:
    log_lines = file.readlines()

# 解析日志数据
times = []
battery_levels = []

for line in log_lines:
    # 使用正则表达式匹配时间戳和电池数据
    match = re.search(r'(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*?battery_level: \[(\d+),', line)
    if match:
        time_str = match.group(1)
        level = int(match.group(2))

        # 将字符串转换为datetime对象
        time_obj = datetime.strptime(f"2025-{time_str}", '%Y-%m-%d %H:%M:%S.%f')

        times.append(time_obj)
        battery_levels.append(level)

# 创建图表
plt.figure(figsize=(12, 6), dpi=100)
plt.plot(times, battery_levels, marker='o', markersize=3, linestyle='-', linewidth=1.5, color='b')

# 设置标题和标签
plt.title('Battery Level Over Time', fontsize=14)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Battery Level (%)', fontsize=12)

# 格式化时间轴
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
plt.gcf().autofmt_xdate()

# 设置Y轴范围
plt.ylim(0, max(battery_levels) + 5)

# 添加网格
plt.grid(True, linestyle='--', alpha=0.7)

# 高亮显示充电区域
# charge_start = None
# for i in range(1, len(battery_levels)):
#     if battery_levels[i] > battery_levels[i - 1]:
#         charge_start = times[i - 1]
#         break
#
# if charge_start:
#     plt.axvspan(charge_start, times[-1], alpha=0.2, color='green', label='Charging Phase')
#     plt.legend()

plt.tight_layout()
plt.savefig('battery_level_plot.png', bbox_inches='tight')
plt.show()