#!/usr/bin/env python3
import subprocess
import random
import time
import os

# Target IP address
TARGET_IP = "10.45.0.1"

# Function to delete a route for the target IP
def delete_route():
    cmd = ["ip", "route", "del", "default"]
    print(f"Removing route: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error removing route: {e}")

def add_route(interface):
    cmd = ["ip", "route", "add", "default", "dev", interface]
    print(f"Adding route: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error adding route for {interface}: {e}")

# Function to run hping3 with specified parameters
def run_hping3(interface, interval):

    # Delete the existing route for the target IP
    delete_route()
    
    # Add route for the target IP through the specified interface
    add_route(interface)

    cmd = [
        "hping3",
        "-1",              # UDP mode
        TARGET_IP,         # Target IP
        "-i", f"u{interval}",       # Inter-packet interval in microseconds
        "-c", str(random.randint(10,5000))  # Number of packets to send
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
        interface_list = ['uesimtun0', 'uesimtun1', 'uesimtun2', 'uesimtun3', 'uesimtun4', 'uesimtun5', 'uesimtun6', 'uesimtun7', 'uesimtun8', 'uesimtun9']
        # Randomly select an interface from the list
        interface = random.choice(interface_list)
        # Set inter-packet interval (random between 2000 and 5000 microseconds)
        interval = random.randint(200, 500)
        
        # Run hping3
        process = run_hping3(interface, interval)
        time.sleep(1)
        
        # Terminate the hping3 process
        process.terminate()
        try:
            process.wait(timeout=1)  # Wait briefly for clean exit
        except subprocess.TimeoutExpired:
            process.kill()  # Force kill if it doesn't exit

        time.sleep(1)
        

except KeyboardInterrupt:
    print("\nStopped by user.")
except Exception as e:
    print(f"Error: {e}")