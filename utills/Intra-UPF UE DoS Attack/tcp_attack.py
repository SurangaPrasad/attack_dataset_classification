#!/usr/bin/env python3
import subprocess
import random
import time
import os

# Target IP address
TARGET_IP = "10.45.0.32" # User IP

# Function to run hping3 with specified parameters
def run_hping3(port, count, interval):
    cmd = [
        "hping3",
        "-p", str(port),   # Port number
        TARGET_IP,         # Target IP
        "-S",             # TCP SYN flag
        "-c", str(count),     # Number of packets to send
        "-i", f"u{interval}" ,      # Inter-packet interval in microseconds
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
        port = 8080
        
        # Set random packet count
        count = random.randint(1, 100)
        
        # Set inter-packet interval (random between 2000 and 5000 microseconds)
        interval = random.randint(2000, 5000)
        
        # Run hping3
        process = run_hping3(port, count, interval)
        
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