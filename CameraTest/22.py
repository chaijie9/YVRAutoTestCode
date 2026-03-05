import re
import matplotlib.pyplot as plt

# 从文件中读取日志内容
with open(r"D:\cjcj.txt", "r",encoding="utf16") as file:
    log_content = file.read()

    # 定义正则表达式模式
    pattern = r'\((\w+)\):\[dur: avg:(\d+\.\d+), min:(\d+\.\d+), max:(\d+\.\d+)\)\] \[lat: avg:(\d+\.\d+), min:(\d+\.\d+), max:(\d+\.\d+)\], miss\((\d+)\) total:(\d+)'

    # 使用正则表达式模式搜索日志内容
    matches = re.findall(pattern, log_content)

    # 初始化存储统计量的字典
    sensor_stats = {}

    # 遍历匹配结果，将数据按传感器类型分组
    for match in matches:
        sensor, avg_dur, min_dur, max_dur, avg_lat, min_lat, max_lat, miss, total = match
        if sensor not in sensor_stats:
            sensor_stats[sensor] = {
                "avg_dur": [],
                "min_dur": [],
                "max_dur": [],
                "avg_lat": [],
                "min_lat": [],
                "max_lat": []
            }
        sensor_stats[sensor]["avg_dur"].append(float(avg_dur))
        sensor_stats[sensor]["min_dur"].append(float(min_dur))
        sensor_stats[sensor]["max_dur"].append(float(max_dur))
        sensor_stats[sensor]["avg_lat"].append(float(avg_lat))
        sensor_stats[sensor]["min_lat"].append(float(min_lat))
        sensor_stats[sensor]["max_lat"].append(float(max_lat))

    # 计算每个传感器的最大值、最小值和平均值
    sensor_max_values = {}
    sensor_min_values = {}
    sensor_avg_values = {}

    for sensor, stats in sensor_stats.items():
        sensor_max_values[sensor] = {
            "max_dur": max(stats["max_dur"]),
            "max_lat": max(stats["max_lat"])
        }
        sensor_min_values[sensor] = {
            "min_dur": min(stats["min_dur"]),
            "min_lat": min(stats["min_lat"])
        }
        sensor_avg_values[sensor] = {
            "avg_dur": sum(stats["avg_dur"]) / len(stats["avg_dur"]),
            "avg_lat": sum(stats["avg_lat"]) / len(stats["avg_lat"])
        }


    # 打印结果
    print("Max Values per Sensor:")
    print(sensor_max_values)
    print("\nMin Values per Sensor:")
    print(sensor_min_values)
    print("\nAverage Values per Sensor:")
    print(sensor_avg_values)
# =============================================================================

    # 丢帧
    miss_counts = {}
    # 初始化存储传感器数据的字典
    sensor_data = {}

    # 遍历匹配结果，将数据按传感器类型统计丢失数量和丢失次数
    for match in matches:
        sensor, avg_dur, min_dur, max_dur, avg_lat, min_lat, max_lat, miss, total = match
        if sensor not in miss_counts:
            miss_counts[sensor] = {
                "miss_sum": 0,
                "count": 0
            }
        if int(miss) != 0:
            miss_counts[sensor]["miss_sum"] += int(miss)
            miss_counts[sensor]["count"] += 1

    # 打印每个传感器的丢失数量和丢失次数
    for sensor, counts in miss_counts.items():
        print(f"Sensor: {sensor}")
        print(f"Total Misses: {counts['miss_sum']}")
        print(f"Total Counts: {counts['count']}\n")
    # =============================================================================

    # 遍历匹配结果，将数据按传感器类型存储
    for match in matches:
        sensor, avg_dur, min_dur, max_dur, avg_lat, min_lat, max_lat, miss, total = match
        if sensor not in sensor_data:
            sensor_data[sensor] = {
                "lat": []
            }
        sensor_data[sensor]["lat"].append(float(avg_lat))

    # 绘制折线图
    for sensor, data in sensor_data.items():
        plt.plot(data["lat"], label=sensor)
    # 添加图例和标签
    plt.xlabel('Index')
    plt.ylabel('Average Latency')
    plt.title('Average Latency of Sensors')
    plt.legend()
    plt.grid(True)
    plt.ylim(0, 20)  # 设置 y 轴的范围和间隔
    # plt.yticks([i*2 for i in range(0, 41, 1)])
    # 显示图形
    plt.show()

