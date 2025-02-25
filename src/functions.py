import time
import threading
import sys
import random

lock = threading.RLock()
condition = threading.Condition(lock)

def simulate_sensor(recorded_temps: dict[list]) -> None:
    """
        Simulates temperature readings from multiple sensors and updates the shared data structure.

        Each sensor generates a random temperature reading between 15°C and 40°C every second.
        The function acquires a lock to safely modify the shared `recorded_temps` dictionary.
        Once updated, it signals `process_temperatures` that new data is available.

        Args:
            recorded_temps (dict[list]): A dictionary where each key represents a sensor ID,
                                         and each value is a list of recorded temperature readings.

        Synchronization:
            - Uses `lock` (RLock) to ensure thread-safe access to `recorded_temps`.
            - Calls `condition.notify_all()` to wake up the processing thread.
        """
    while True:
        with lock:
            for sensor_number in recorded_temps.keys():
                recorded_temps[sensor_number].append(random.randint(15, 40))
            condition.notify_all()
        time.sleep(1)

def avg(nums: list[int]) -> float:
    """
        Computes the average of a list of numbers, rounded to two decimal places.

        If the list is empty, it returns 0.00 to prevent division errors.

        Args:
            nums (list[int]): A list of numerical values.

        Returns:
            float: The average of the list rounded to two decimal places.
        """
    return round(sum(nums) / len(nums) if nums else 0, 2)

def process_temperatures(recorded_temps: dict, temperature_avg: dict) -> None:
    """
        Waits for new temperature readings and updates the average temperature for each sensor.

        The function remains in a loop, waiting for a signal from `simulate_sensor` indicating
        that new temperature data is available. Once signaled, it calculates and updates
        the average temperature for each sensor.

        Args:
            recorded_temps (dict): A dictionary mapping sensor IDs to lists of recorded temperatures.
            temperature_avg (dict): A dictionary mapping sensor IDs to their computed average temperatures.

        Synchronization:
            - Uses `condition.wait()` to pause until new data is available.
            - Uses `lock` (via `condition`) to ensure thread-safe access to shared data.
        """
    while True:
        with condition:
            condition.wait()

            for sensor_number in recorded_temps.keys():
                temperature_avg[sensor_number] = avg(recorded_temps[sensor_number])

def update_display(recorded_temps: dict, temperature_avg: dict) -> None:
    """
        Continuously updates the console display with the latest temperature readings and averages.

        The function retrieves and formats the most recent temperature readings and their
        corresponding averages, then updates the console output without clearing the screen.

        Args:
            recorded_temps (dict): A dictionary mapping sensor IDs to lists of recorded temperatures.
            temperature_avg (dict): A dictionary mapping sensor IDs to their computed average temperatures.

        Synchronization:
            - Uses `lock` to safely read from shared data structures.
            - Prevents race conditions while retrieving temperature values.

        Console Behavior:
            - Uses ANSI escape sequences (`\033[F`) to update the output in place.
            - Ensures a clean, readable format without overwriting new lines.
        """
    print("\n" * 100)
    while True:
        with lock:
            results = [
                f"Current Temperatures:",
                f"Latest Temperatures: "
            ]

            for i in range(len(recorded_temps)):
                latest_temp = recorded_temps[i][-1] if recorded_temps[i] else "--"
                avg_temp = f"{temperature_avg.get(i, '--'):.2f}" if isinstance(temperature_avg.get(i),
                                                                               (int, float)) else "--"

                results[1] += f"Sensor {i}: {latest_temp}°C  "
                results.append(f"Sensor {i} Average: {avg_temp}°C")

            sys.stdout.write("\033[F" * len(results))
            sys.stdout.write("\r" + "\n".join(results) + "\n")
            sys.stdout.flush()
        time.sleep(1)
