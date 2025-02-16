from time import time
from src.functions import sumNum

def run_sequentially(num:int):
    """Computes the time it took for the program to run both functions.

    Arguments:
        int: Number of test cases you want to use.
    
    Returns:
        float: Time it took for the functions to run (in seconds)
    """
    start = time()
    total = sumNum(1, num, None)
    end = time()
    timeTaken = end - start
    
    return timeTaken, total