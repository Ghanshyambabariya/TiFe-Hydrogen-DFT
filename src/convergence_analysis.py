from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def load_convergence_table(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    rows = []
    for ecut in [30, 40, 50, 60]:
        rows.append({"parameter": "ecutwfc", "value": ecut, "mesh": "6x6x6", "total_energy_eV": "", "calculation_status": "Calculation pending"})
    for mesh in ["4x4x4", "6x6x6", "8x8x8"]:
        rows.append({"parameter": "kpoints", "value": mesh, "mesh": mesh, "total_energy_eV": "", "calculation_status": "Calculation pending"})
    df = pd.DataFrame(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def pending_plot(path: Path, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.text(0.5, 0.55, "Calculation pending", ha="center", va="center", fontsize=16, weight="bold")
    ax.text(0.5, 0.42, "Run the Quantum ESPRESSO inputs and add parsed energies.", ha="center", va="center")
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_if_available(df: pd.DataFrame, parameter: str, path: Path, title: str, xlabel: str) -> None:
    subset = df[df["parameter"] == parameter].copy()
    numeric = pd.to_numeric(subset["total_energy_eV"], errors="coerce")
    if numeric.notna().sum() < 2:
        pending_plot(path, title)
        return
    fig, ax = plt.subplots(figsize=(6.5, 4.0))
    ax.plot(subset["value"].astype(str), numeric, marker="o", color="#2f5d8c")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Total energy (eV)")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main() -> None:
    df = load_convergence_table(ROOT / "results" / "convergence_summary.csv")
    plot_if_available(df, "ecutwfc", ROOT / "figures" / "energy_vs_cutoff.png", "Energy convergence with plane-wave cutoff", "ecutwfc (Ry)")
    plot_if_available(df, "kpoints", ROOT / "figures" / "energy_vs_kpoints.png", "Energy convergence with k-point mesh", "k-point mesh")


if __name__ == "__main__":
    main()
