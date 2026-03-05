from matplotlib import pyplot as plt
#
# res_list = []

res_list1 = []

# f = open("./新休眠唤醒.txt", "r")
# result = f.readlines()
# for n in result:
#     r_n = n.replace('\n', '')
#     res_list.append(int(r_n))
#     f.close()
# print(res_list)
# print(max(res_list))
# print(min(res_list))
# print(sum(res_list) / len(res_list))

fig,ax = plt.subplots()
res_list2 = []
print("====================================================")
f = open("./旧休眠唤醒.txt", "r")
result = f.readlines()
for n in result:
    r_n = n.replace('\n', '')
    res_list1.append(int(r_n))
    f.close()

f = open("./新休眠唤醒.txt", "r")
result = f.readlines()
for n in result:
    r_n = n.replace('\n', '')
    res_list2.append(int(r_n))
    f.close()
#
ax.set_ylim([0,130])

plt.plot(res_list1, "x-", label="migration time", color="g" )
plt.plot(res_list2,"+-", label="request delay",  color="r",)
plt.show()
# import os
# import time
# test_count = 0
# while True:
#     power_onoff = "adb shell input keyevent POWER"
#     os.system(power_onoff)
#     time.sleep(10)
#     test_count += 0.5
#     print(test_count)


