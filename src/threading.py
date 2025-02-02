from time import time
from threading import Thread
from src.functions import joinChar, sumNum
from math import ceil
from os import cpu_count

def run_threads(num: int) -> float:
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
    
    sumThreads = []
    charThreads = []
    
    for chunk in chunks:
        start_chunk, end_chunk = chunk
        charThread = Thread(target=joinChar, args=(start_chunk, end_chunk))
        charThreads.append(charThread)
        charThread.start()
        
        sumThread = Thread(target=sumNum, args=(start_chunk, end_chunk))
        sumThreads.append(charThread)
        sumThread.start()

    
    for thread in charThreads:
        thread.join()
        
    for thread in sumThreads:
        thread.join()
    
    end = time()
    
    timeTaken = end - start
    
    return timeTaken