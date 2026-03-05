import re
import matplotlib.pyplot as plt

# 存储pss值的列表
pss_values = []

# 逐行读取文件内容
with open('./result.txt', 'r') as file:
    for line in file.readlines():
        # 使用正则表达式匹配pss的值
        match = re.search(r'pss:(\d+)KB', line)
        if match:
            pss_values.append(int(match.group(1)))

# 生成x轴数据，即数据点的索引
print(pss_values)
x = range(len(pss_values))

# 绘制折线图
plt.plot(x, pss_values)
plt.xlabel('Data Point Index')
plt.ylabel('PSS Value (KB)')
plt.title('PSS Values Over Time')
plt.show()