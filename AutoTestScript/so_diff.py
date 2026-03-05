# # -*- coding: utf-8 -*-
# import os
# import sys
#
#
# def get_so_files_info(folder):
#     """收集文件夹中所有.so文件的相对路径和大小"""
#     so_files = {}
#     for root, _, files in os.walk(folder):
#         for file in files:
#             if file.endswith('.so'):
#                 full_path = os.path.join(root, file)
#                 rel_path = os.path.relpath(full_path, folder)
#                 size = os.path.getsize(full_path)
#                 so_files[rel_path] = size
#     return so_files
#
#
# def main(folder1, folder2):
#     # 获取两个文件夹的.so文件信息
#     so_info1 = get_so_files_info(folder1)
#     so_info2 = get_so_files_info(folder2)
#
#     # 获取文件集合
#     common_files = set(so_info1.keys()) & set(so_info2.keys())
#     only_in1 = set(so_info1.keys()) - set(so_info2.keys())
#     only_in2 = set(so_info2.keys()) - set(so_info1.keys())
#
#     # 比较共同文件的大小
#     same_files = []
#     diff_files = []
#     for file in common_files:
#         size1 = so_info1[file]
#         size2 = so_info2[file]
#         if size1 == size2:
#             same_files.append((file, size1))
#         else:
#             diff_files.append((file, size1, size2))
#
#     # 输出结果
#     print(f"比较文件夹: '{folder1}' 和 '{folder2}'")
#     print(
#         f"扫描到 {len(common_files)} 个共同文件, {len(only_in1)} 个仅存在于第一个文件夹, {len(only_in2)} 个仅存在于第二个文件夹")
#
#     if same_files:
#         print("\n大小相同的文件:")
#         for file, size in same_files:
#             print(f"  ✓ {file}: {size} bytes")
#
#     if diff_files:
#         print("\n大小不同的文件:")
#         for file, size1, size2 in diff_files:
#             print(f"  ✗ {file}: {size1} bytes vs {size2} bytes")
#
#     if only_in1:
#         print("\n仅存在于第一个文件夹的文件:")
#         for file in only_in1:
#             print(f"  ? {file}: {so_info1[file]} bytes")
#
#     if only_in2:
#         print("\n仅存在于第二个文件夹的文件:")
#         for file in only_in2:
#             print(f"  ? {file}: {so_info2[file]} bytes")
#
#     # 返回状态码
#     return 0 if not diff_files and not only_in1 and not only_in2 else 1
#
#
# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("用法: python compare_so.py <文件夹1> <文件夹2>")
#         sys.exit(1)
#
#     folder1 = sys.argv[1]
#     folder2 = sys.argv[2]
#
#     if not os.path.isdir(folder1) or not os.path.isdir(folder2):
#         print("错误: 提供的路径必须是文件夹")
#         sys.exit(1)
#
#     exit_code = main(folder1, folder2)
#     print(f"\n比较完成 (状态: {'成功' if exit_code == 0 else '有差异'})")
#     sys.exit(exit_code)
# from sys import platform
import platform
import subprocess


def run_adb_command(command, capture_output=True, timeout=30):
    """执行ADB命令并返回结果"""
    full_cmd = f"adb -s 192.168.8.119:5555  {command}"
    try:
        result = subprocess.run(
            full_cmd,
            shell=True,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',  # 明确指定编码
            timeout=timeout
        )
        return result.stdout.strip() if capture_output else None
    except subprocess.TimeoutExpired:
        print(f"命令超时: {full_cmd}")
        return None
    except Exception as e:
        print(f"命令执行错误: {e}")
        return None


grep_cmd = 'findstr' if platform.system() == 'Windows' else 'grep'


def check_log_for_keyword(keyword):
    """检查日志中是否包含关键词"""
    log_output = run_adb_command(f"logcat -d | {grep_cmd} \"{keyword}\"")
    return keyword in log_output if log_output else False


init_success =check_log_for_keyword("6DOF is ready!!!!!!")
print(init_success)