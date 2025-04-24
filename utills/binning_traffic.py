import os
import time
import random

# Define traffic data (Mbps)
traffic_data = [
    # Low usage (0-10 min)
    5, 4.8, 4.5, 4.2, 3.8, 3.5, 3, 2.8, 2.5, 2.3,  
    # Increasing usage (10-20 min)
    2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.3, 6.5,  
    # High usage (20-30 min)
    6.6, 6.4, 6.8, 6.7, 6.8, 7, 6.9, 6.9, 7.1, 7.2,  
    # Peak usage (30-40 min)
    7.3, 7.1, 7, 6.9, 6.8, 6.7, 6.7, 6.6, 6.7, 6.8,  
    # Decreasing usage (40-50 min)
    6.9, 7, 7.2, 7.3, 7.8, 8.5, 8.6, 9, 8.9, 8.5,  
    # Low usage again (50-60 min)
    8, 7.3, 6.8, 5.5, 4.5, 4.2, 4, 3.8, 3.5, 3
]

# Target server (update with the correct IP/hostname)
server_ip = "10.42.0.99"  # Change this to the actual iPerf3 server IP
#run this 10 times
for i in range(10):
    for bitrate in traffic_data:
        # Add a small random variation (0 - 0.2 Mbps)
        random_variation = random.uniform(0, 0.2)
        adjusted_bitrate = round(bitrate + random_variation, 2)

        # Convert Mbps to Kbps for iperf3
        bitrate_kbps = int(adjusted_bitrate * 1000)

        # Run iperf3 command (for one minute)
        cmd = f"iperf3 -c {server_ip} -b {bitrate_kbps}K -t 60"
        print(f"Running: {cmd}")
        
        os.system(cmd)  # Execute the command

    print("Traffic pattern execution completed.")
