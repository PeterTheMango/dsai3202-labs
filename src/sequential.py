from random import choice, randint
from string import ascii_letters
from time import time
from src.functions import joinChar, sumNum

def run_sequentially(num:int):
    """Computes the time it took for the program to run both functions.

    Arguments:
        int: Number of test cases you want to use.
    
    Returns:
        float: Time it took for the functions to run (in seconds)
    """
    start = time()
    joinChar(1, num)
    sumNum(1, num)
    end = time()
    timeTaken = end - start
    
    return timeTaken