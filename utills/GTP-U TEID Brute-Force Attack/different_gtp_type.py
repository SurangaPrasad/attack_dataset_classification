#!/usr/bin/env python3
from scapy.all import IP, UDP, send
from scapy.contrib.gtp import GTPHeader
import random
import time

def random_teid():
    return random.randint(1, 1000000)

def send_packet_with_random_teid():
    pkt = (
        IP(src="10.42.0.108", dst="10.42.0.64") /
        UDP(sport=2152, dport=2152) /
        GTPHeader(version=1, PT=1, gtp_type=1, teid=random_teid()) /  # T-PDU
        IP(src="10.45.0.42", dst="8.8.8.8") /
        UDP(sport=12345, dport=53)  # Inner UDP packet to elicit a response
    )
    return pkt

packet_count = 0
max_packets = 10000
while packet_count < max_packets:
    pkt = send_packet_with_random_teid()
    send(pkt, count=1, inter=0.01, verbose=1)  # Slower rate to observe responses
    packet_count += 1
    time.sleep(0.01)