import threading
import queue
from src.functions import simulate_sensor, process_temperatures, update_display, initialize_display

# Dictionary to store the temperature sensors.
latest_temperatures = {}
temperature_averages = {}
temperature_queues = {} 

# Storing the threads.
threads = []

# Main Program
if __name__ == "__main__":
    # Deciding the number of sensors.
    num_sensors = int(input("Enter the number of sensors: "))
 
    # Initializing the data.
    for sensor_id in range(num_sensors):
        latest_temperatures[sensor_id] = None
        temperature_averages[sensor_id] = 0
        temperature_queues[sensor_id] = queue.Queue()

    # Starting the diplay.
    initialize_display(latest_temperatures, temperature_averages)

    # Adding the threads to the list.
    threads.append(threading.Thread(target=simulate_sensor, args=(num_sensors, latest_temperatures, temperature_queues), daemon=True))
    threads.append(threading.Thread(target=process_temperatures, args=(temperature_queues, temperature_averages), daemon=True))
    threads.append(threading.Thread(target=update_display, args=(latest_temperatures, temperature_averages), daemon=True))

    # Starting the threads.
    for thread in threads:
        thread.start()

    # Waiting for the threads to finish.
    for thread in threads:
        thread.join()
