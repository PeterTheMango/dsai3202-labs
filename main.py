import threading
from src.functions import simulate_sensor, process_temperatures, update_display

# Dictionary to store the temperature sensors.
recorded_temps = dict()
temperature_avg = dict()

# Storing the threads.
threads = []

# Main Program
if __name__ == "__main__":
    # Deciding the number of sensors.
    num_sensors = int(input("Enter the number of sensors: "))
 
    # Initializing the data.
    for i in range(num_sensors):
        recorded_temps[i] = []
        temperature_avg[i] = "--"

    # Adding the threads to the list.
    threads.append(threading.Thread(target=update_display, args=(recorded_temps, temperature_avg), daemon=True))
    threads.append(threading.Thread(target=simulate_sensor, args=(recorded_temps,), daemon=True))
    threads.append(threading.Thread(target=process_temperatures, args=(recorded_temps, temperature_avg), daemon=True))

    # Starting the threads.
    for thread in threads:
        thread.start()

    # Waiting for the threads to finish.
    for thread in threads:
        thread.join()
