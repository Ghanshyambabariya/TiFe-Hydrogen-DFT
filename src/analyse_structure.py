from __future__ import annotations

from pathlib import Path

import pandas as pd

from add_hydrogen import HYDROGEN_SITES
from build_supercell import build_tife_supercell
from structure_io import add_atom, nearest_distances


ROOT = Path(__file__).resolve().parents[1]


def pending_summary() -> pd.DataFrame:
    supercell = build_tife_supercell()
    rows = []
    for label, frac in HYDROGEN_SITES.items():
        structure = add_atom(supercell, "H", frac, label)
        h_index = len(structure.symbols) - 1
        ti_distances = nearest_distances(structure, h_index, "Ti", n=4)
        fe_distances = nearest_distances(structure, h_index, "Fe", n=4)
        nearest_ti = min(ti_distances) if ti_distances else ""
        nearest_fe = min(fe_distances) if fe_distances else ""
        rows.append(
            {
                "site": label,
                "total_energy_eV": "",
                "relative_energy_eV": "",
                "nearest_Ti_H_distance_A": nearest_ti,
                "nearest_Fe_H_distance_A": nearest_fe,
                "cell_volume_A3": structure.volume,
                "volume_change_percent": "",
                "calculation_status": "Calculation pending",
                "candidate_fractional_position": f"({frac[0]:.3f}, {frac[1]:.3f}, {frac[2]:.3f})",
                "mean_four_Ti_H_distance_A": sum(ti_distances) / len(ti_distances) if ti_distances else "",
                "mean_four_Fe_H_distance_A": sum(fe_distances) / len(fe_distances) if fe_distances else "",
                "geometric_note": "Initial unrelaxed geometry only; not a site-stability result.",
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    out = ROOT / "results" / "h_interstitial_summary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    pending_summary().to_csv(out, index=False)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
