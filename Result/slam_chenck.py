import pandas as pd
import matplotlib.pyplot as plt

# 读取txt文件，假设文件以空格分隔


import matplotlib.pyplot as plt

with open(r'C:\Users\chaijie\Desktop\0816\OrcaNext_7c30a30f290d4dc69ce367be2ce7f62429c888a3\controller_2024-08-22-04-30-00\vio_time_consume2.txt', 'r') as f:
    lines = f.readlines()



plt.plot(lines)
plt.xlabel('Data Points')
plt.ylabel('Values')
plt.title('Line Chart of Second Values in Txt')
plt.show()