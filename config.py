import os
from algorithm import cholesky_sequential

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE_DIR, "results")
RESULTS_CSV = os.path.join(OUTDIR, "results.csv")
TABLES_MD = os.path.join(OUTDIR, "tables.md")

SEED = 42
SIZES = [100 * i for i in range(1, 14)]
PROCS = [1, 2, 4]
REPEATS = 3

ALGORITHMS_TO_RUN = ["sequential"]
ALGORITHMS = {
    "sequential": {"func": cholesky_sequential, "parallel": False},

    # "threads":   {"func": cholesky_threads,   "parallel": True},
    # "processes": {"func": cholesky_processes, "parallel": True},
}
BASELINE_ALGORITHM = "sequential"

RESIDUAL_TOL = 1e-9

CALIBRATION_N0 = 300
TARGET_TIME_S = 120.0

RUN_CALIBRATION = False
RUN_BENCHMARK = True
RUN_ANALYSIS = True
OVERWRITE_RESULTS = True

RESULTS_COLUMNS = [
    "run_id", "algorithm",
    "n", "p",
    "repeat", "time_s",
    "residual_fro", "residual_rel",
    "ok", "cpu_count",
]
