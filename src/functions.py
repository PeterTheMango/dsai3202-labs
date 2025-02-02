from random import choice, randint
from string import ascii_letters

def joinChar(start: int, end: int) -> str:
    """Generates a random string of ascii letters based on the range from start to end.

    Args:
        start (int): Starting index (not used here directly).
        end (int): Ending index, determines the length of the string to generate.

    Returns:
        str: Random string of length `end - start + 1`.
    """
    return "".join([choice(ascii_letters) for _ in range(end - start + 1)])

def sumNum(start: int, end: int):
    """Computes the sum of random numbers based on the range from start to end.

    Args:
        start (int): Starting index (not used directly).
        end (int): Ending index, determines how many random numbers to sum.

    Returns:
        int: Sum of `end - start + 1` random integers.
    """
    return sum([randint(1, 100) for _ in range(end - start + 1)])