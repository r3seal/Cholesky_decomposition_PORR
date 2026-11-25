import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import BASELINE_ALGORITHM, OUTDIR


def plot_sequential_time(agg):
    seq = agg[(agg["algorithm"] == BASELINE_ALGORITHM) & (agg["p"] == 1)]
    seq = seq.sort_values("n")
    if seq.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(seq["n"], seq["time_s"], marker="o")
    ax.set_title("Wersja sekwencyjna: czas od rozmiaru")
    ax.set_xlabel("wymiar macierzy")
    ax.set_ylabel("czas T [s]")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, "time_sequential.png"), dpi=150)
    plt.close(fig)


def plot_time_3d(agg, algorithm):
    sub = agg[agg["algorithm"] == algorithm]
    if sub.empty:
        return

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection="3d")

    for n in sorted(sub["n"].unique()):
        punkty = sub[sub["n"] == n].sort_values("p")
        ax.plot(punkty["p"], [n] * len(punkty), punkty["time_s"],
                marker="o", label=f"n = {n}")

    ax.set_title(f"{algorithm}: czas w zależności od n i p")
    ax.set_xlabel("liczba procesów/wątków p")
    ax.set_ylabel("rozmiar zadania n")
    ax.set_zlabel("czas T [s]")
    ax.set_xticks(sorted(sub["p"].unique()))
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, f"time3d_{algorithm}.png"), dpi=150)
    plt.close(fig)


def make_plots(agg):
    # jeżeli sekwencyjny to czas od wymiaru
    # jeżeli niesekwencyjny to czas od wymiaru i liczby procesów
    os.makedirs(OUTDIR, exist_ok=True)
    plot_sequential_time(agg)
    for algorithm in sorted(agg["algorithm"].unique()):
        if algorithm != BASELINE_ALGORITHM:
            plot_time_3d(agg, algorithm)