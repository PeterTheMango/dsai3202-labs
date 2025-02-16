from time import time
from multiprocessing import Process, Queue
from os import cpu_count
from math import ceil
from src.functions import sumNum


def run_processes(num):
    """Computes the time it took for the program to run both functions.

    Arguments:
        int: Number of test cases you want to use.
    
    Returns:
        float: Time it took for the functions to run (in seconds)
    """
    
    total_start = time()
    
    num_cores = cpu_count()
    chunk_size = ceil(num / num_cores)
    chunks = [(i * chunk_size, min((i + 1) * chunk_size, num)) for i in range(num_cores)]
    
    results = Queue()
    
    start = time()
    
    sum_processes = []
    
    for chunk in chunks:
        start_chunk, end_chunk = chunk
        sum_process = Process(target=sumNum, args=(start_chunk, end_chunk, results))
        sum_processes.append(sum_process)
        sum_process.start()
        
    for proc in sum_processes:
        proc.join()
    
    end = time()
    
    time_taken = end - start
    total = 0
    while not results.empty():
        total += results.get()
    
    total_end = time()
    
    total_time = total_end - total_start
    speedup = time_taken/total_time
    
    return (time_taken, speedup, total)