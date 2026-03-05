import subprocess
import argparse
import re
import matplotlib.pyplot as plt
import csv
from collections import defaultdict
from datetime import datetime
from matplotlib import rcParams

# ANSI转义字符清理
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def clean_ansi(text):
    return ansi_escape.sub('', text)


# 配置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
rcParams['axes.unicode_minus'] = False


def parse_header(header):
    """动态解析列位置"""
    header = clean_ansi(header)
    cols = []
    prev_space = True
    start = 0
    for i, c in enumerate(header):
        if c != ' ' and prev_space:
            start = i
        if c == ' ' and not prev_space:
            cols.append((start, i))
        prev_space = (c == ' ')
    if not prev_space:
        cols.append((start, len(header)))
    return cols


def main():
    parser = argparse.ArgumentParser(description='线程CPU监控工具')
    parser.add_argument('pid', type=int, help='进程PID')
    parser.add_argument('--output', '-o', default='cpu_data.csv', help='输出文件')
    parser.add_argument('--interval', '-i', type=int, default=10, help='采样间隔')
    parser.add_argument('--threads', '-t', nargs='+', help='过滤线程')
    args = parser.parse_args()

    cmd = ['adb', 'shell', 'top', '-H', '-p', str(args.pid), '-d', str(args.interval)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    thread_data = defaultdict(list)
    header_parsed = False
    cols_map = {}

    try:
        with open(args.output, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['时间', '线程名', 'CPU%', 'TID'])

            while True:
                line = proc.stdout.readline()
                if not line:
                    break

                raw_line = clean_ansi(line.decode(errors='replace')).strip()
                print(f"[DEBUG] {raw_line}")  # 调试输出

                # 解析标题行
                if not header_parsed and 'TID' in raw_line and 'S[%CPU]' in raw_line:
                    cols = parse_header(raw_line)
                for idx, (s, e) in enumerate(cols):
                    col_name = raw_line[s:e].strip()
                if col_name == 'TID':
                    cols_map['tid'] = (s, e)
                elif col_name == 'S[%CPU]':
                    cols_map['cpu'] = (s, e)
                elif idx == len(cols) - 1:  # 最后一列为线程名
                    cols_map['name'] = (s, len(raw_line))
                header_parsed = True
                print(f"[HEADER] 列位置: {cols_map}")
                continue

                if header_parsed:
                    try:
                        # 提取TID
                        tid = raw_line[cols_map['tid'][0]:cols_map['tid'][1]].strip()
                        if not tid.isdigit():
                            continue

                        # 提取CPU值（处理"S 14.8"格式）
                        cpu_str = raw_line[cols_map['cpu'][0]:cols_map['cpu'][1]].strip()
                        cpu_val = float(cpu_str.split()[-1])

                        # 提取线程名（处理列尾）
                        name_start = cols_map['name'][0]
                        thread_name = raw_line[name_start:].split()[0].strip()

                        # 线程过滤
                        if args.threads and not any(t in thread_name for t in args.threads):
                            continue

                        # 写入数据
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        writer.writerow([timestamp, thread_name, cpu_val, tid])
                        thread_data[thread_name].append(cpu_val)
                        print(f"[DATA] {thread_name} {cpu_val}%")  # 数据日志

                    except (ValueError, IndexError) as e:
                        print(f"[ERROR] 解析失败: {e}")
                        continue

    except KeyboardInterrupt:
        print("\n停止监控...")
    finally:
        proc.terminate()

    # 生成图表
    if thread_data:
        plt.figure(figsize=(15, 7))
        for name, data in thread_data.items():
            plt.plot(data, label=name, marker='o')

        plt.title(f"进程 {args.pid} CPU使用趋势")
        plt.xlabel(f"采样次数（间隔{args.interval}s）")
        plt.ylabel("CPU使用率 (%)")
        plt.legend(bbox_to_anchor=(1.15, 1))
        plt.grid(linestyle='--', alpha=0.6)

        plot_file = args.output.replace('.csv', '.png')
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {plot_file}")
        plt.show()
    else:
        print("无有效数据，请检查：")
        print("1. ADB连接")
        print("2. 进程状态")
        print("3. 列解析日志")


if __name__ == '__main__':
    main()