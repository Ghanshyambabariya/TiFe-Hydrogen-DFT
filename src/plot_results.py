from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def placeholder(path: Path, title: str, note: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.text(0.5, 0.58, "Calculation pending", ha="center", va="center", fontsize=16, weight="bold")
    ax.text(0.5, 0.43, note, ha="center", va="center")
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_volume_change() -> None:
    summary = ROOT / "results" / "h_interstitial_summary.csv"
    path = ROOT / "figures" / "volume_change.png"
    if not summary.exists():
        placeholder(path, "Volume change after hydrogen insertion", "Run structural analysis after QE relaxation.")
        return
    df = pd.read_csv(summary)
    volume_change = pd.to_numeric(df.get("volume_change_percent"), errors="coerce")
    if volume_change.notna().sum() == 0:
        placeholder(path, "Volume change after hydrogen insertion", "Volume change requires relaxed pristine and H-containing cells.")
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df["site"], volume_change, color="#49796b")
    ax.set_ylabel("Volume change (%)")
    ax.set_title("Structural expansion after hydrogen insertion")
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_bond_distances() -> None:
    summary = ROOT / "results" / "h_interstitial_summary.csv"
    path = ROOT / "figures" / "bond_distance_comparison.png"
    if not summary.exists():
        placeholder(path, "Nearest metal-H distances", "Run structural analysis after QE relaxation.")
        return
    df = pd.read_csv(summary)
    ti = pd.to_numeric(df.get("nearest_Ti_H_distance_A"), errors="coerce")
    fe = pd.to_numeric(df.get("nearest_Fe_H_distance_A"), errors="coerce")
    if ti.notna().sum() == 0 and fe.notna().sum() == 0:
        placeholder(path, "Nearest metal-H distances", "Distances require generated or relaxed H-containing structures.")
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    x = range(len(df))
    ax.plot(x, ti, marker="o", label="nearest Ti-H")
    ax.plot(x, fe, marker="s", label="nearest Fe-H")
    ax.set_xticks(list(x), df["site"], rotation=25, ha="right")
    ax.set_ylabel("Distance (angstrom)")
    ax.set_title("Local metal-H distance comparison")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_dos_placeholders() -> None:
    placeholder(ROOT / "figures" / "dos_TiFe.png", "TiFe density of states", "Optional DOS calculation pending.")
    placeholder(ROOT / "figures" / "dos_TiFe_H.png", "TiFe + H density of states", "Optional DOS calculation pending.")
    placeholder(ROOT / "figures" / "dos_comparison.png", "DOS comparison", "Run QE DOS calculations before interpretation.")


def main() -> None:
    plot_volume_change()
    plot_bond_distances()
    plot_dos_placeholders()


if __name__ == "__main__":
    main()
