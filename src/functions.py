from random import choice, randint
from string import ascii_letters

def sumNum(start: int, end: int):
    """
    Computes the sum of integers within a specified range.

    Args:
        start (int): The starting value of the range (inclusive).
        end (int): The ending value of the range (inclusive).

    Returns:
        int: The sum of all integers from `start` to `end`, inclusive.
    """
    return sum(range(start, end + 1))