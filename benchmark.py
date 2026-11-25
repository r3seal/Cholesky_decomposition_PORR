import datetime
import os
import numpy as np
from tqdm import tqdm

from algorithm import cholesky_sequential
from config import (RESIDUAL_TOL, SEED, TARGET_TIME_S, ALGORITHMS)
from utility import (generate_spd_matrix, measure_time, residual_frobenius,
                     save_result_row)


def run_single(func, a, p):
    timed_func = measure_time(func)
    l, elapsed = timed_func(a, p)
    res_fro = residual_frobenius(a, l)
    res_rel = res_fro / float(np.linalg.norm(a, ord="fro"))
    return elapsed, res_fro, res_rel


def calibrate():
    CALIBRATION_CONSTANT = 100
    time_result = 0
    dimension = 0
    while time_result < TARGET_TIME_S:
        dimension += CALIBRATION_CONSTANT
        a = generate_spd_matrix(dimension)
        _, time_result = measure_time(cholesky_sequential)(a, 1)
        print(f"Wymiar: {dimension}, Czas: {time_result}")
        if time_result > TARGET_TIME_S:
            dimension -= CALIBRATION_CONSTANT

    print(f"Proponowane SIZES w config.py: {[100 * i for i in range(1, dimension+1)]}")


def run_benchmark(algorithm_names, sizes, procs, repeats):
    run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    cpu_count = os.cpu_count() or 1

    plan = []
    for n in sizes:
        for name in algorithm_names:
            p_list = procs if ALGORITHMS[name]["parallel"] else [1]
            for p in p_list:
                for r in range(1, repeats + 1):
                    plan.append((n, name, p, r))

    current_n = None
    a = None
    with tqdm(total=len(plan), desc="Testy", unit="run") as bar:
        for n, name, p, r in plan:
            if n != current_n:
                a = generate_spd_matrix(n, SEED)
                current_n = n
            bar.set_postfix(alg=name, n=n, p=p, rep=r)

            elapsed, res_fro, res_rel = run_single(ALGORITHMS[name]["func"], a, p)
            ok = bool(res_rel < RESIDUAL_TOL)
            if not ok:
                tqdm.write(f"[UWAGA] {name} n={n} p={p}: residuum względne {res_rel:.2e}")

            save_result_row({
                "run_id": run_id, "algorithm": name, "n": n, "p": p, "repeat": r,
                "time_s": elapsed, "residual_fro": res_fro, "residual_rel": res_rel,
                "ok": ok, "cpu_count": cpu_count,
            })
            bar.update(1)
