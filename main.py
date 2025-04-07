from mpi4py import MPI
import numpy as np
import sys
import multiprocessing
import time
from functools import partial

def square_wrapper(rank, num):
    print(f"[Rank {rank}] Squaring number: {num}")
    return num ** 2

def parallel_square_worker(start, time_limit, rank):
    num_workers = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_workers)

    start_time = time.time()
    result = []
    count = 0

    # Use functools.partial to pass rank to the wrapper
    wrapped_square = partial(square_wrapper, rank)

    while time.time() - start_time < time_limit:
        result.append(pool.apply(wrapped_square, args=(start,)))
        count += 1
        start += 1

    pool.close()
    pool.join()

    return result, count

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    time_limit = 10  # seconds

    start_number = 1 + rank

    squares, count = parallel_square_worker(start_number, time_limit, rank)

    all_squares = comm.gather(squares, root=0)
    all_counts = comm.gather(count, root=0)

    if rank == 0:
        result = [item for sublist in all_squares for item in sublist]
        total_count = sum(all_counts)

        highest_square = max(result) if result else 0

        print("\n===== Summary =====")
        print(f"Highest square computed: {highest_square}")
        print(f"Total squares computed: {total_count}")
        print(f"Time limit of {time_limit} seconds reached.")

if __name__ == '__main__':
    main()
