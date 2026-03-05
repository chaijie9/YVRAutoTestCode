import subprocess
import time
count = 0
while True:
    subprocess.call("adb shell cat sys/class/kgsl/kgsl-3d0/gpu_busy_percentage >> 11.txt", shell=True)
    time.sleep(1)
    count += 1
    if count >= 120:
        break