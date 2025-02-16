from time import time
from threading import Thread
from src.functions import sumNum
from math import ceil
from os import cpu_count

def run_threads(num: int) -> float:
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
    
    start = time()
    
    sumThreads = []
    
    for chunk in chunks:
        start_chunk, end_chunk = chunk
        sumThread = Thread(target=sumNum, args=(start_chunk, end_chunk))
        sumThreads.append(sumThread)
        sumThread.start()
        
    for thread in sumThreads:
        thread.join()
    
    end = time()
    
    time_taken = end - start
    
    total_end = time()
    
    total_time = total_end - total_start
    speedup = time_taken/total_time
    
    return (time_taken, speedup)