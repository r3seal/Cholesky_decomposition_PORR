import math
import numpy as np


def cholesky_sequential(a_in, p=1):
    a = np.array(a_in, dtype=np.float64, copy=True)
    n = a.shape[0]

    for k in range(n - 1):
        a[k, k] = math.sqrt(a[k, k])
        lkk = a[k, k]
        for i in range(k + 1, n):
            a[i, k] = a[i, k] / lkk

        for j in range(k + 1, n):
            ljk = a[j, k]
            for i in range(j, n):
                a[i, j] = a[i, j] - a[i, k] * ljk

    a[n - 1, n - 1] = math.sqrt(a[n - 1, n - 1])

    return np.tril(a)
