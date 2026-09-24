from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np


RY_TO_EV = 13.605693122994


def parse_qe_output(path: str | Path) -> dict:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    result: dict = {"source": str(path), "calculation_status": "unknown"}

    energies = re.findall(r"!\s+total energy\s+=\s+([-0-9.]+)\s+Ry", text)
    if energies:
        result["total_energy_Ry"] = float(energies[-1])
        result["total_energy_eV"] = float(energies[-1]) * RY_TO_EV

    lattice = re.findall(r"lattice parameter \(alat\)\s+=\s+([-0-9.]+)\s+a\.u\.", text)
    if lattice:
        result["alat_au"] = float(lattice[-1])

    volume = re.findall(r"unit-cell volume\s+=\s+([-0-9.]+)\s+\(a\.u\.\)\^3", text)
    if volume:
        bohr_to_ang = 0.529177210903
        result["cell_volume_A3"] = float(volume[-1]) * bohr_to_ang**3

    if "JOB DONE." in text:
        result["calculation_status"] = "completed"
    elif "convergence NOT achieved" in text:
        result["calculation_status"] = "not_converged"

    cell = parse_last_cell_parameters(text)
    if cell is not None:
        result["cell_A"] = cell.tolist()
        result["cell_volume_A3"] = float(abs(np.linalg.det(cell)))

    atoms = parse_last_atomic_positions(text)
    if atoms:
        result["atomic_positions_A"] = atoms

    return result


def parse_last_cell_parameters(text: str) -> np.ndarray | None:
    blocks = re.findall(r"CELL_PARAMETERS\s+\(?angstrom\)?\s*\n((?:\s*[-0-9.Ee]+\s+[-0-9.Ee]+\s+[-0-9.Ee]+\s*\n){3})", text)
    if not blocks:
        return None
    rows = [[float(value) for value in line.split()[:3]] for line in blocks[-1].strip().splitlines()]
    return np.array(rows, dtype=float)


def parse_last_atomic_positions(text: str) -> list[dict]:
    blocks = re.findall(r"ATOMIC_POSITIONS\s+\(?angstrom\)?\s*\n((?:\s*[A-Za-z]+\s+[-0-9.Ee]+\s+[-0-9.Ee]+\s+[-0-9.Ee]+.*\n)+)", text)
    if not blocks:
        return []
    atoms = []
    for line in blocks[-1].strip().splitlines():
        parts = line.split()
        if len(parts) >= 4:
            atoms.append({"symbol": parts[0], "x": float(parts[1]), "y": float(parts[2]), "z": float(parts[3])})
    return atoms


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse selected values from a Quantum ESPRESSO output file.")
    parser.add_argument("output", help="Quantum ESPRESSO .out file")
    parser.add_argument("--json", default=None, help="Optional JSON output path")
    args = parser.parse_args()
    parsed = parse_qe_output(args.output)
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(parsed, indent=2), encoding="utf-8")
    print(json.dumps(parsed, indent=2))


if __name__ == "__main__":
    main()
