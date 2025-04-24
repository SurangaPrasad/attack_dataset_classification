#!/usr/bin/env python3
import subprocess
import random
import time

TARGET_IP = "10.45.0.32"  # Target UE IP

def run_hping3(count, interval):
    cmd = [
        "hping3",
        "-1",  # ICMP mode
        TARGET_IP,
        "-c", str(count),  # Number of packets
        "-i", f"u{interval}",  # Inter-packet interval in microseconds
        "-d", str(random.randint(500,1500)),  # Data size
    ]
    print(f"Running: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return process

try:
    while True:
        count = random.randint(50, 200)
        interval = random.randint(1000, 3000)  # 1-3ms interval
        process = run_hping3(count, interval)
        time.sleep(1)
        process.terminate()
        process.wait(timeout=1)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped by user.")