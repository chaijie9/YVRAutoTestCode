import subprocess
import time
# count = 0
# while True:
#     subprocess.call("adb shell cat sys/class/kgsl/kgsl-3d0/gpu_busy_percentage >> 11.txt", shell=True)
#     time.sleep(1)
#     count += 1
#     if count >= 120:
#         break
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R

# 读取 TUM 格式的文件
file_path = r'C:\Users\chaijie\6dof二期验收\files-1F\SLAM_2024_11_05_02_35_38.txt'
with open(file_path, 'r') as f:
    lines = f.readlines()

# 提取时间戳、位置和四元数数据
timestamps = []
tx = []
ty = []
tz = []
qx = []
qy = []
qz = []
qw = []

for line in lines:
    parts = line.strip().split()
    if len(parts) == 8:  # TUM 格式行包含时间戳和位姿信息
        timestamps.append(float(parts[0]))
        tx.append(float(parts[1]))
        ty.append(float(parts[2]))
        tz.append(float(parts[3]))
        qx.append(float(parts[4]))
        qy.append(float(parts[5]))
        qz.append(float(parts[6]))
        qw.append(float(parts[7]))

# 转换为 DataFrame
df = pd.DataFrame({
    'timestamp': timestamps,
    'tx': tx,
    'ty': ty,
    'tz': tz,
    'qx': qx,
    'qy': qy,
    'qz': qz,
    'qw': qw
})

# 定义一个函数将四元数转换为欧拉角 (roll, pitch, yaw)
def quat_to_euler(quat):
    r = R.from_quat([quat[0], quat[1], quat[2], quat[3]])
    euler = r.as_euler('xyz', degrees=True)  # 'xyz' 表示欧拉角顺序
    return euler

# 计算每个时间戳的 roll, pitch, yaw
euler_angles = df[['qx', 'qy', 'qz', 'qw']].apply(lambda x: quat_to_euler(x), axis=1)
df[['roll', 'pitch', 'yaw']] = pd.DataFrame(euler_angles.tolist(), index=df.index)

# 假设我们要查询时间范围 [start_time, end_time]
start_time = 40  # 设置开始时间
end_time = 80   # 设置结束时间

# 筛选出时间段内的数据
filtered_data = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]

# 获取在该时间段内的位置和欧拉角的最大值与最小值
max_values = filtered_data[['tx', 'ty', 'tz', 'roll', 'pitch', 'yaw']].max()
min_values = filtered_data[['tx', 'ty', 'tz', 'roll', 'pitch', 'yaw']].min()

# 计算最大值和最小值的差
difference = max_values - min_values

print("Max values in the time range:")
print(max_values)
print("\nMin values in the time range:")
print(min_values)
print("\nDifference between Max and Min values:")
print(difference)