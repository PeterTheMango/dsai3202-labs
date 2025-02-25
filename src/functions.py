import time
import threading
import sys
import random
import queue

lock = threading.RLock()
condition = threading.Condition(lock)
MAX_QUEUE_SIZE = 15

def simulate_sensor(num_sensors: int, latest_temperatures: dict[int, int], temperature_queues: dict[int, queue.Queue]) -> None:
    """
    Simulates temperature sensors by generating random temperatures.
    
    Args:
        num_sensors (int): Number of sensors to simulate.
        latest_temperatures (dict[int, int]): Dictionary to store latest temperatures.
        temperature_queues (dict[int, queue.Queue]): Dictionary of queues storing temperature readings.
    
    Returns:
        None
    """
    time.sleep(3)  # Simulating sensor connection and startup.
    
    while True:
        with lock:
            for sensor_number in range(num_sensors):
                temp = random.randint(15, 40)
                latest_temperatures[sensor_number] = temp
                
                if temperature_queues[sensor_number].qsize() >= MAX_QUEUE_SIZE:
                    temperature_queues[sensor_number].get()
                
                temperature_queues[sensor_number].put(temp)
            condition.notify_all()
        time.sleep(1)

def avg(nums: list[int]) -> float:
    """
    Computes the average of a list of numbers.
    
    Args:
        nums (list[int]): List of temperature readings.
    
    Returns:
        float: The average temperature rounded to 2 decimal places.
    """
    return round(sum(nums) / len(nums) if nums else 0, 2)

def process_temperatures(temperature_queues: dict[int, queue.Queue], temperature_averages: dict[int, float]) -> None:
    """
    Processes temperature data by computing averages from sensor queues.
    
    Args:
        temperature_queues (dict[int, queue.Queue]): Dictionary of temperature queues.
        temperature_averages (dict[int, float]): Dictionary storing average temperatures.
    
    Returns:
        None
    """
    while True:
        with condition:
            condition.wait()
            with lock:
                for sensor_number, temp_queue in temperature_queues.items():
                    readings = list(temp_queue.queue)
                    temperature_averages[sensor_number] = avg(readings)

def update_latest_temp(latest_temperatures: dict[int, int], start_line: int) -> None:
    """
    Updates and displays the latest temperature readings.
    
    Args:
        latest_temperatures (dict[int, int]): Dictionary containing latest temperatures.
        start_line (int): The starting line for updating the display.
    
    Returns:
        None
    """
    while True:
        with lock:
            sys.stdout.write(f"\033[{start_line};0H")
            sys.stdout.write("\033[K")
            sys.stdout.write("Latest Temperatures: ")
            
            for sensor_id in latest_temperatures.keys():
                latest_temp = latest_temperatures[sensor_id] if latest_temperatures[sensor_id] is not None else "--"
                sys.stdout.write(f"Sensor {sensor_id}: {latest_temp}°C  ")
            
            sys.stdout.write("\n")
            sys.stdout.write("\033[" + str(len(latest_temperatures)) + "B")
            sys.stdout.flush()
        
        time.sleep(1)

def update_avg_temps(temperature_averages: dict[int, float], start_line: int) -> None:
    """
    Updates and displays the average temperatures.
    
    Args:
        temperature_averages (dict[int, float]): Dictionary containing temperature averages.
        start_line (int): The starting line for updating the display.
    
    Returns:
        None
    """
    while True:
        with lock:
            sys.stdout.write(f"\033[{start_line};0H")
            sys.stdout.write("\033[K")
            
            for sensor_id in temperature_averages.keys():
                avg_temp = f"{temperature_averages[sensor_id]:.2f}" if temperature_averages[sensor_id] > 0 else "--"
                sys.stdout.write(f"Sensor {sensor_id} Average: {avg_temp}°C  ")
                sys.stdout.write("\n")
                
            sys.stdout.write("\033[" + str(len(temperature_averages)) + "B")
            sys.stdout.flush()
        
        time.sleep(5)

def update_display(latest_temperatures: dict[int, int], temperature_averages: dict[int, float]) -> None:
    """
    Manages threads for updating the latest and average temperature displays.
    
    Args:
        latest_temperatures (dict[int, int]): Dictionary containing latest temperatures.
        temperature_averages (dict[int, float]): Dictionary containing temperature averages.
    
    Returns:
        None
    """
    latest_temp_start_line = 4 
    avg_temp_start_line = 5

    threads = [
        threading.Thread(target=update_latest_temp, args=(latest_temperatures, latest_temp_start_line), daemon=True),
        threading.Thread(target=update_avg_temps, args=(temperature_averages, avg_temp_start_line), daemon=True)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def initialize_display(latest_temperatures: dict[int, int], temperature_averages: dict[int, float]) -> None:
    """
    Initializes the terminal display for temperature readings.
    
    Args:
        latest_temperatures (dict[int, int]): Dictionary containing latest temperatures.
        temperature_averages (dict[int, float]): Dictionary containing temperature averages.
    
    Returns:
        None
    """
    print("Current temperatures:")
    print("Latest Temperatures: ", end="")
    for sensor_id in latest_temperatures.keys():
        print(f"Sensor {sensor_id}: --°C ", end="")
    print()
    for sensor_id in temperature_averages.keys():
        print(f"Sensor {sensor_id} Average: --°C ")
