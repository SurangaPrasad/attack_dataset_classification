#!/usr/bin/env python3

import random
import subprocess
import time
import re

# Configuration
IPERF_SERVER = "10.42.0.99"  # Your iperf3 server IP
INTERFACES = [f"uesimtun{i}" for i in range(10)]  # 10 interfaces: uesimtun0 to uesimtun9
MIN_THROUGHPUT_MBPS = 5
MAX_THROUGHPUT_MBPS = 50
MIN_DURATION_SECS = 10
MAX_DURATION_SECS = 60
TOTAL_ITERATIONS = 50
SLEEP_BETWEEN_TESTS = 2

def get_interface_ips():
    """Retrieve IP addresses for each uesimtunX interface."""
    interface_ips = {}
    try:
        # Run 'ip addr' to get interface details
        output = subprocess.check_output(["ip", "addr"], text=True)
        for interface in INTERFACES:
            # Look for lines like "inet 10.45.0.30/24 brd 10.45.0.255 scope global uesimtun7"
            pattern = rf"inet (\d+\.\d+\.\d+\.\d+)/\d+.*{interface}"
            match = re.search(pattern, output)
            if match:
                ip = match.group(1)
                interface_ips[interface] = ip
                print(f"Found IP for {interface}: {ip}")
            else:
                print(f"Warning: No IP found for {interface}")
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving IP addresses: {e}")
    return interface_ips

def run_iperf3(interface, source_ip, throughput_mbps, duration_secs):
    """Run iperf3 using the source IP of the specified interface."""
    cmd = [
        "iperf3", "-c", IPERF_SERVER, "-B", source_ip,
        "-t", str(duration_secs), "-b", f"{throughput_mbps}M",
        "-P", "1", "--verbose"
    ]
    print(f"Running iperf3 via {interface} (source IP {source_ip}): {throughput_mbps} Mbps for {duration_secs} seconds")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Output:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running iperf3 on {interface}: {e.stderr}")
        return False

def simulate_video_traffic(interface_ips):
    """Simulate video streaming traffic across available interfaces."""
    if not interface_ips:
        print("No interfaces with IPs found. Exiting.")
        exit(1)

    available_interfaces = list(interface_ips.keys())
    for iteration in range(TOTAL_ITERATIONS):
        interface = random.choice(available_interfaces)
        source_ip = interface_ips[interface]
        throughput_mbps = random.randint(MIN_THROUGHPUT_MBPS, MAX_THROUGHPUT_MBPS)
        duration_secs = random.randint(MIN_DURATION_SECS, MAX_DURATION_SECS)
        
        success = run_iperf3(interface, source_ip, throughput_mbps, duration_secs)
        if success:
            sleep_time = random.uniform(0, SLEEP_BETWEEN_TESTS)
            print(f"Sleeping for {sleep_time:.2f} seconds before next test...")
            time.sleep(sleep_time)
        print(f"Completed iteration {iteration + 1}/{TOTAL_ITERATIONS}\n")

if __name__ == "__main__":
    print("Starting video streaming simulation with iperf3...")
    
    # Get IP addresses dynamically
    interface_ips = get_interface_ips()
    
    # Run the simulation with available interfaces
    try:
        simulate_video_traffic(interface_ips)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    finally:
        print("Simulation completed.")