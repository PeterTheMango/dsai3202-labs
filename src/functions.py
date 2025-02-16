from random import choice, randint
from string import ascii_letters

def sumNum(start: int, end: int, queue):
    """
    Computes the sum of integers within a specified range.

    Args:
        start (int): The starting value of the range (inclusive).
        end (int): The ending value of the range (inclusive).

    Returns:
        None
    """
    if(queue == None):
        return sum(range(start, end + 1))
    else:
        ans = sum(range(start, end + 1))
        queue.put(ans)