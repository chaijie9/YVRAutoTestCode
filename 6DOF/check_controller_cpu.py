import re

from matplotlib import pyplot as plt

# res_list = []
# source_file = r'D:\新桌面\1.5冷启动.txt'
# with open(source_file, 'r') as f:
#     line = f.readlines()
#     for n in line:
#         r_n = n.replace('\n', '')
#         if "ALG_IMU_Thread" in r_n:
#             # print(r_n)
#             cpu = re.findall(r"[SR]( .*)\s", r_n)
#             # print(cpu)
#             res_list.append((float(cpu[0][1:5])))
#
#     print(max(res_list))
#     print(min(res_list))
#     print(sum(res_list) / len(res_list))


res_list = []
source_file = r'C:\Users\chaijie\CC.txt'
with open(source_file, 'r') as f:
    line = f.readlines()
    for n in line:
        r_n = n.replace('\n', '')
        if "MESH_I" in r_n:
            print(r_n)
            cpu = re.findall(r"[SR]( .*)\s", r_n)
            res_list.append((float(cpu[0][1:5])))
    print(res_list)

    print(max(res_list))
    print(min(res_list))
    print(sum(res_list) / len(res_list))
plt.plot(res_list)
ax=plt.gca()
# ax.xaxis.set_major_locator(x_major_locator)
# ax.yaxis.set_major_locator(y_major_locator)
plt.xlabel('')
plt.ylabel('MESH_Image')
# plt.xlim(0, 210)
ax.set_ylim([0,70])
# plt.savefig(file_name.replace("txt", "jpg"))

plt.show()
