#!/usr/bin/env python3
from scapy.all import IP, UDP, send
from scapy.contrib.gtp import GTPHeader
import random

# Function to generate a random IP address
def random_ip():
    first_octet = 10
    return f"{first_octet}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Function to craft and send a packet with a random source IP
def send_packet_with_random_ip():
    # Craft the packet with a random source IP
    pkt = (
        IP(src=random_ip(), dst="10.42.0.64") /
        UDP(sport=2152, dport=2152) /
        GTPHeader(version=1, PT=1, gtp_type=1, teid=12345) # Valid GTP header without inner IP packet
        # GTPHeader(version=2, PT=1, gtp_type=1, teid=12345) # Invalid version Number
        # GTPHeader(version=1, PT=1, gtp_type=0, teid=12345)  # Invalid gtp_type (0 is not defined)
        # GTPHeader(version=1, PT=1, gtp_type=1, teid=12345, E=1, S=1, PN=1)  # Set E/S/PN flags
        # GTPHeader(version=1, PT=1, gtp_type=1, teid=12345, length=1000) /  # Oversized length
    )
    return pkt

# Send packets in a loop with random source IPs
while True:  # Loop indefinitely (replace with a condition if needed)
    pkt = send_packet_with_random_ip()
    send(pkt, count=random.randint(0,10), inter=0.0002, verbose=1)