import subprocess
import time

# Define the command to run
command = "nr-ue -c ue.yaml -i 001010000000300"

# Define the timing parameters
max_duration = 60  # Time to run the flood (in seconds)
rest_duration = 600  # Rest period (in seconds) -> 10 minutes
num_cycles = 10  # Number of times to repeat
log_file = "execution_log.txt"  # Log file name

# Open the log file for writing
with open(log_file, "a") as log:
    try:
        for cycle in range(num_cycles):
            start_time = time.time()  # Record start time

            log.write(f"Cycle {cycle + 1}/{num_cycles} started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"Starting cycle {cycle + 1}/{num_cycles}...")

            # Run processes for max_duration seconds
            while time.time() - start_time <= max_duration:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(0.8)  # Wait for 0.8 seconds before starting the next process

            log.write(f"Cycle {cycle + 1} completed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            print(f"Cycle {cycle + 1} completed. Resting for {rest_duration // 60} minutes...\n")

            time.sleep(rest_duration)  # Rest for 10 minutes

        log.write("All cycles completed.\n")
        print("All cycles completed.")

    except KeyboardInterrupt:
        log.write("Script terminated by user.\n")
        print("Script terminated by user.")
