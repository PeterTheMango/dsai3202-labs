from time import time
from multiprocessing import Process
from os import cpu_count
from math import ceil
from src.functions import joinChar, sumNum


def run_processes(num):
    """Computes the time it took for the program to run both functions.

    Arguments:
        int: Number of test cases you want to use.
    
    Returns:
        float: Time it took for the functions to run (in seconds)
    """
    
    num_cores = cpu_count() 
    chunk_size = ceil(num / num_cores)
    chunks = [(i * chunk_size, min((i + 1) * chunk_size, num)) for i in range(num_cores)]
    
    start = time()
    
    sum_processes = []
    char_processes = []
    
    for chunk in chunks:
        start_chunk, end_chunk = chunk
        char_process = Process(target=joinChar, args=(start_chunk, end_chunk))
        char_processes.append(char_process)
        char_process.start()
        
        sum_process = Process(target=sumNum, args=(start_chunk, end_chunk))
        sum_processes.append(char_process)
        sum_process.start()

    
    for proc in char_processes:
        proc.join()
        
    for proc in sum_processes:
        proc.join()
    
    end = time()
    
    timeTaken = end - start
    
    return timeTaken