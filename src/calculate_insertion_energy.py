from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def calculate_table() -> pd.DataFrame:
    summary_path = ROOT / "results" / "h_interstitial_summary.csv"
    if not summary_path.exists():
        return pd.DataFrame(
            columns=[
                "site",
                "E_Ti8Fe8H_eV",
                "E_Ti8Fe8_eV",
                "E_H2_eV",
                "E_insert_eV",
                "relative_E_insert_eV",
                "calculation_status",
            ]
        )
    sites = pd.read_csv(summary_path)
    rows = []
    for _, row in sites.iterrows():
        rows.append(
            {
                "site": row["site"],
                "E_Ti8Fe8H_eV": row.get("total_energy_eV", ""),
                "E_Ti8Fe8_eV": "",
                "E_H2_eV": "",
                "E_insert_eV": "",
                "relative_E_insert_eV": "",
                "calculation_status": "Calculation pending",
            }
        )
    return pd.DataFrame(rows)


def plot_insertion(table: pd.DataFrame) -> None:
    path = ROOT / "figures" / "hydrogen_site_energy_comparison.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    energy = pd.to_numeric(table.get("E_insert_eV", pd.Series(dtype=float)), errors="coerce")
    if table.empty or energy.notna().sum() == 0:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.text(0.5, 0.55, "Calculation pending", ha="center", va="center", fontsize=16, weight="bold")
        ax.text(0.5, 0.42, "Insertion energies require E(Ti8Fe8H), E(Ti8Fe8), and E(H2).", ha="center", va="center")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    else:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(table["site"], energy, color="#8a5a2b")
        ax.set_ylabel("Hydrogen insertion energy (eV)")
        ax.set_title("Hydrogen site energy comparison")
        ax.tick_params(axis="x", rotation=25)
        ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def main() -> None:
    table = calculate_table()
    out = ROOT / "results" / "hydrogen_insertion_energies.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out, index=False)
    plot_insertion(table)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
