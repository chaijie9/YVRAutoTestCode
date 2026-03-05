import numpy as np

# 第一个数据点位置
tx1, ty1, tz1 = -0.538865, -0.285925 ,0.195825  # 位置

# 第二个数据点位置
tx2, ty2, tz2 =   -0.508249, -0.275417, 0.230282  # 位置

# 计算位置差值
delta_tx = tx2 - tx1
delta_ty = ty2 - ty1
delta_tz = tz2 - tz1

# 计算位置之间的欧几里得距离
distance_position = np.sqrt(delta_tx**2 + delta_ty**2 + delta_tz**2)

# 输出结果
print(f"Position difference: {distance_position:.6f} ")