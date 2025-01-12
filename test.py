import time

import numpy as np

# Create large arrays
size = 10_000_00000

# Default integer array (int64)
arr_default = np.random.randint(0, 256, size, dtype=np.int64)

# uint8 array
arr_uint8 = np.array(arr_default, dtype=np.uint8)

# uint16 array
arr_uint16 = np.array(arr_default, dtype=np.uint16)

# Measure operation time
start = time.time()
result_default = arr_default + 1
print(f"Default int64 time: {time.time() - start:.6f} seconds")

start = time.time()
result_uint8 = arr_uint8 + 1
print(f"uint8 time: {time.time() - start:.6f} seconds")

start = time.time()
result_uint16 = arr_uint16 + 1
print(f"uint16 time: {time.time() - start:.6f} seconds")
