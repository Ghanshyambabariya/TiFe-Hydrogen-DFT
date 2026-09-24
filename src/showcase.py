from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def load_summary() -> pd.DataFrame:
    path = ROOT / "results" / "h_interstitial_summary.csv"
    if not path.exists():
        raise FileNotFoundError("Run python src/run_workflow_setup.py before creating the showcase.")
    return pd.read_csv(path)


def plot_distance_screening(df: pd.DataFrame) -> None:
    path = ROOT / "figures" / "interstitial_distance_screening.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    labels = [label.replace("Site_", "").replace("_", "\n") for label in df["site"]]
    ti = pd.to_numeric(df["nearest_Ti_H_distance_A"], errors="coerce")
    fe = pd.to_numeric(df["nearest_Fe_H_distance_A"], errors="coerce")
    x = range(len(df))

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.bar([i - 0.18 for i in x], ti, width=0.36, label="nearest Ti-H", color="#5b8db8")
    ax.bar([i + 0.18 for i in x], fe, width=0.36, label="nearest Fe-H", color="#b7794b")
    ax.set_xticks(list(x), labels)
    ax.set_ylabel("Initial distance (angstrom)")
    ax.set_title("Unrelaxed geometric screening of H starting sites")
    ax.text(
        0.5,
        -0.23,
        "Distances are from generated starting structures only. Energetic stability requires QE relaxation.",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=9,
        color="#56616f",
    )
    ax.grid(axis="y", alpha=0.22)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def plot_workflow_overview() -> None:
    path = ROOT / "figures" / "dft_workflow_overview.png"
    stages = [
        ("Build B2 TiFe", "Ti corner\nFe body centre"),
        ("Create Ti8Fe8", "2 x 2 x 2\nsupercell"),
        ("Insert H", "siteA / siteB / siteC\nstarting points"),
        ("Run QE", "relaxation +\nconvergence checks"),
        ("Analyse", "relative energy\nlocal distances\nvolume change"),
    ]
    fig, ax = plt.subplots(figsize=(11, 3.8))
    ax.set_xlim(0, len(stages))
    ax.set_ylim(0, 1)
    ax.axis("off")
    for i, (title, body) in enumerate(stages):
        x = i + 0.1
        box = plt.Rectangle((x, 0.26), 0.78, 0.46, facecolor="#f4f7fb", edgecolor="#8aa0b8", linewidth=1.4)
        ax.add_patch(box)
        ax.text(x + 0.39, 0.58, title, ha="center", va="center", fontsize=11, weight="bold", color="#1f3147")
        ax.text(x + 0.39, 0.42, body, ha="center", va="center", fontsize=9.5, color="#46566a")
        if i < len(stages) - 1:
            ax.annotate("", xy=(i + 1.03, 0.49), xytext=(i + 0.90, 0.49), arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#62758c"})
    ax.text(0.5, 0.08, "Current repository state: executable setup and pending-result analysis framework; no fabricated QE outputs.", ha="center", va="center", transform=ax.transAxes, fontsize=9.5, color="#6a7480")
    fig.tight_layout()
    fig.savefig(path, dpi=220)
    plt.close(fig)


def write_showcase(df: pd.DataFrame) -> None:
    path = ROOT / "docs" / "showcase.md"
    rows = []
    for _, row in df.iterrows():
        rows.append(
            f"| `{row['site']}` | `{row['candidate_fractional_position']}` | "
            f"`{float(row['nearest_Ti_H_distance_A']):.3f}` | `{float(row['nearest_Fe_H_distance_A']):.3f}` | "
            f"{row['calculation_status']} |"
        )
    content = f"""# Project Showcase

This page summarizes what the repository can currently demonstrate without pretending that full Quantum ESPRESSO calculations have already been completed.

## Current Demonstrable Outputs

- B2-TiFe primitive structure generated from explicit fractional positions.
- `2 x 2 x 2` Ti8Fe8 supercell generated reproducibly.
- Three candidate H interstitial starting structures created as CIF/XYZ files.
- Quantum ESPRESSO input templates for pristine relaxation, convergence checks, H-site relaxation, H2 reference, and optional DOS.
- Parser and analysis scripts prepared for real QE outputs.
- Result CSVs intentionally marked `Calculation pending` where DFT execution is still required.

![DFT workflow overview](../figures/dft_workflow_overview.png)

## Geometric Pre-Screening

The table below reports distances from the generated, unrelaxed starting geometries. These values are useful for explaining the candidate-site construction, but they are not DFT stability results.

| Site | Fractional H start | nearest Ti-H (A) | nearest Fe-H (A) | Status |
|---|---:|---:|---:|---|
{chr(10).join(rows)}

![Interstitial distance screening](../figures/interstitial_distance_screening.png)

## What Requires Quantum ESPRESSO Execution

The following outputs cannot be claimed until the corresponding QE calculations are run and parsed:

- optimized lattice parameter
- final total energies
- relative H-site energies
- hydrogen insertion energies
- relaxed volume change
- DOS and projected DOS interpretation

## Best Interview Framing

This project is best presented as a careful exploratory workflow: structure construction, first-principles input preparation, convergence awareness, and analysis scaffolding for hydrogen incorporation in TiFe. The scientifically honest result at this stage is that the computational framework is ready, while full energetic conclusions are pending actual DFT execution.
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    df = load_summary()
    plot_distance_screening(df)
    plot_workflow_overview()
    write_showcase(df)


if __name__ == "__main__":
    main()
