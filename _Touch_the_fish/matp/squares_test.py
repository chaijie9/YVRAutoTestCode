'''
15-1 立方：数字的三次方被称为其立方。请绘制一个图形，显示前 5 个整数的立方
值，再绘制一个图形，显示前 5000 个整数的立方值。
15-2 彩色立方：给你前面绘制的立方图指定颜色映射。
'''
from matplotlib import pyplot as plt

x_values = list(range(1, 5000))
y_values = [x ** 3 for x in x_values]

plt.title("test_mode")
plt.xlabel("x轴")
plt.ylabel("y轴")

plt.scatter(x_values, y_values, c="Yellow", edgecolors="none", s= 40)
plt.axis([0, 1000, 0, 1000000000])
plt.show()
plt.savefig()