import os

from analysis import analyze
from benchmark import calibrate, run_benchmark
from config import (ALGORITHMS_TO_RUN, ALGORITHMS, BASELINE_ALGORITHM, OUTDIR, OVERWRITE_RESULTS,
                    PROCS, REPEATS, RESULTS_CSV, RUN_ANALYSIS, RUN_BENCHMARK,
                    RUN_CALIBRATION, SIZES)


def main():
    os.makedirs(OUTDIR, exist_ok=True)

    if RUN_CALIBRATION:
        calibrate()

    if RUN_BENCHMARK:
        unknown = [a for a in ALGORITHMS_TO_RUN if a not in ALGORITHMS]
        if unknown:
            raise SystemExit(f"Nieznane algorytmy w config.ALGORITHMS_TO_RUN: {unknown}. "
                             f"Dostępne (registry.py): {sorted(ALGORITHMS)}")

        if OVERWRITE_RESULTS and os.path.exists(RESULTS_CSV):
            os.remove(RESULTS_CSV)

        names = [BASELINE_ALGORITHM] + [a for a in ALGORITHMS_TO_RUN if a != BASELINE_ALGORITHM]
        run_benchmark(names, sorted(SIZES), sorted(set(PROCS)), REPEATS)

    if RUN_ANALYSIS:
        if not os.path.exists(RESULTS_CSV):
            raise SystemExit(f"Brak pliku {RESULTS_CSV}")
        analyze()

if __name__ == "__main__":
    main()
