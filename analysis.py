import pandas as pd
from plots import make_plots
from config import RESULTS_CSV


def aggregate_results(df):
    return df.groupby(["algorithm", "n", "p"], as_index=False).agg(
        time_s=("time_s", "median"),
        residual_rel_max=("residual_rel", "max"),
        all_ok=("ok", "all"),
    )


def analyze():
    df = pd.read_csv(RESULTS_CSV)
    agg = aggregate_results(df)

    print("\nWyniki (mediana czasu z powtórzeń):")
    print(agg.to_string(index=False))

    make_plots(agg)
    return agg