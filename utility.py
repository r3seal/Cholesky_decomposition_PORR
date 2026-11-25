import functools
import os
import time
import numpy as np
import pandas as pd
from config import OUTDIR, RESULTS_COLUMNS, RESULTS_CSV, SEED

def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        return result, end_time - start_time
    return wrapper

def generate_spd_matrix(n, seed=SEED):
    rng = np.random.default_rng([seed, n])
    g = rng.random((n, n))
    return g.T @ g

def residual_frobenius(a, l):
    return float(np.linalg.norm(l @ l.T - a, ord="fro"))

def save_result_row(row):
    os.makedirs(OUTDIR, exist_ok=True)
    write_header = not os.path.exists(RESULTS_CSV) or os.path.getsize(RESULTS_CSV) == 0
    df = pd.DataFrame([row], columns=RESULTS_COLUMNS)
    df.to_csv(RESULTS_CSV, mode="a", header=write_header, index=False)
