from src import process,sequential, threading
from os import cpu_count

test_cases = 1000000000

sequentialTime, seq_total = sequential.run_sequentially(test_cases)
parallelTime, parallel_speedup, par_total = threading.run_threads(test_cases)
processTime, process_speedup, proc_total = process.run_processes(test_cases)

print(f"=== Total Calculated ===")
print(f"Sequential: {seq_total}")
print(f"Parallel: {par_total}")
print(f"Multiprocessing: {proc_total}")

print(f"Time analysis done according to {test_cases} items.")

print(f"=== Sequential Time Analysis ===")
print(f"Time it took: {sequentialTime} seconds.")

print(f"=== Parallel Time Analysis ===")
print(f"Time it took: {parallelTime} seconds.")

print(f"=== Multi Processing Time Analysis ===")
print(f"Time it took: {processTime} seconds.")

par_seq_speedup = sequentialTime/parallelTime
seq_prc_speedup = sequentialTime/processTime
par_mlt_speedup = parallelTime/processTime

print(f"=== Speedup Analysis ===")
print(f"Speedup from sequential to parallel: {par_seq_speedup}")
print(f"Speedup from sequential to multiprocess: {seq_prc_speedup}")
print(f"Speedup from parallel to multiprocess: {par_mlt_speedup}")

cores = cpu_count()

eff_seq_par = par_seq_speedup / cores
eff_seq_mlt = seq_prc_speedup / cores
eff_par_mlt = par_mlt_speedup / cores

print(f"=== Efficiency Analysis ===")
print(f"Efficiency of sequential to parallel: {eff_seq_par}")
print(f"Efficiency of sequential to multiprocess: {eff_seq_mlt}")
print(f"Efficiency of parallel to multiprocess: {eff_par_mlt}")

print(f"=== Amdahl Speedup Analysis ===")
print(f"Amdahl Parallel Speedup: {parallel_speedup}")
print(f"Amdahl Process Speedup: {process_speedup}")

print(f"=== Gustafsson Speedup Analysis ===")
print(f"Gustafsson Parallel Speedup: {cores - (1- par_seq_speedup) * (cores - 1)}")
print(f"Gustafsson Process Speedup: {cores - (1- seq_prc_speedup) * (cores - 1)}")