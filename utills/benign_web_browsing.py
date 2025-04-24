#!/usr/bin/env python3

import random
import subprocess
import time
import re

# Configuration
URLS = [
    "https://www.wikipedia.org",
    "https://www.bbc.com",
    "https://www.cnn.com",
    "https://www.nytimes.com",
    "https://www.theguardian.com",
    "https://www.reddit.com",
    "https://www.stackoverflow.com",
    "https://www.github.com",
    "https://www.medium.com",
    "https://www.aljazeera.com",
    "http://speedtest.ftp.otenet.gr/files/test100Mb.db",
    "http://download.thinkbroadband.com/100MB.zip"
]
INTERFACES = [f"uesimtun{i}" for i in range(10)]  # 10 interfaces: uesimtun0 to uesimtun9
TOTAL_ITERATIONS = 1000  # Number of browsing requests
MIN_DELAY_SECS = 1     # Minimum delay between requests
MAX_DELAY_SECS = 5     # Maximum delay to mimic user browsing

def get_interface_ips():
    """Retrieve IP addresses for each uesimtunX interface."""
    interface_ips = {}
    try:
        output = subprocess.check_output(["ip", "addr"], text=True)
        for interface in INTERFACES:
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

def run_curl(interface, source_ip, url):
    """Run curl to simulate web browsing using the specified interface's source IP."""
    cmd = [
        "curl",
        "-s",  # Silent mode
        "--interface", interface,  # Bind to the specific interface
        "--max-time", "30",  # Timeout after 30 seconds
        "--insecure",  # Allow self-signed certs (if testing locally)
        url,
        "-o", "/dev/null"  # Discard output to focus on traffic
    ]
    print(f"Fetching {url} via {interface} (source IP {source_ip})")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Success: {url} fetched")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error fetching {url} on {interface}: {e.stderr}")
        return False

def simulate_web_browsing(interface_ips):
    """Simulate web browsing traffic across available interfaces."""
    if not interface_ips:
        print("No interfaces with IPs found. Exiting.")
        exit(1)

    available_interfaces = list(interface_ips.keys())
    for iteration in range(TOTAL_ITERATIONS):
        interface = random.choice(available_interfaces)
        source_ip = interface_ips[interface]
        url = random.choice(URLS)
        
        success = run_curl(interface, source_ip, url)
        if success:
            delay = random.uniform(MIN_DELAY_SECS, MAX_DELAY_SECS)
            print(f"Sleeping for {delay:.2f} seconds before next request...")
            time.sleep(delay)
        print(f"Completed iteration {iteration + 1}/{TOTAL_ITERATIONS}\n")

if __name__ == "__main__":
    print("Starting web browsing simulation with curl...")
    
    # Get IP addresses dynamically
    interface_ips = get_interface_ips()
    
    # Run the simulation with available interfaces
    try:
        simulate_web_browsing(interface_ips)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    finally:
        print("Simulation completed.")