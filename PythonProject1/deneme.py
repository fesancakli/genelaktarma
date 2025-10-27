import numpy as np
import time

# Rastgele matrisler
A = np.random.rand(500, 500)
B = np.random.rand(500, 500)

# --- NumPy matmul
start = time.time()
C1 = np.matmul(A, B)
print("NumPy matmul süresi:", time.time() - start)

# --- For loop (naive Python)
start = time.time()
C2 = np.zeros((500, 500))
for i in range(500):
    for j in range(500):
        for k in range(500):
            C2[i, j] += A[i, k] * B[k, j]
print("For loop süresi:", time.time() - start)

print("Sonuçlar aynı mı:", np.allclose(C1, C2))
