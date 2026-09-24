from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass
class Structure:
    symbols: list[str]
    positions: np.ndarray
    cell: np.ndarray
    comment: str = ""

    @property
    def volume(self) -> float:
        return float(abs(np.linalg.det(self.cell)))

    def copy(self) -> "Structure":
        return Structure(list(self.symbols), self.positions.copy(), self.cell.copy(), self.comment)


def b2_tife(a: float = 2.97) -> Structure:
    cell = np.eye(3) * a
    symbols = ["Ti", "Fe"]
    positions = np.array([[0.0, 0.0, 0.0], [0.5 * a, 0.5 * a, 0.5 * a]], dtype=float)
    return Structure(symbols, positions, cell, "B2 TiFe: Ti at cube corner, Fe at body centre")


def make_supercell(structure: Structure, repeats: tuple[int, int, int] = (2, 2, 2)) -> Structure:
    rx, ry, rz = repeats
    base = structure.cell
    new_cell = base.copy()
    new_cell[0] *= rx
    new_cell[1] *= ry
    new_cell[2] *= rz
    symbols: list[str] = []
    positions: list[np.ndarray] = []
    for ix in range(rx):
        for iy in range(ry):
            for iz in range(rz):
                shift = ix * base[0] + iy * base[1] + iz * base[2]
                for symbol, pos in zip(structure.symbols, structure.positions):
                    symbols.append(symbol)
                    positions.append(pos + shift)
    return Structure(symbols, np.array(positions), new_cell, f"{rx}x{ry}x{rz} supercell of {structure.comment}")


def add_atom(structure: Structure, symbol: str, fractional_position: Iterable[float], label: str) -> Structure:
    out = structure.copy()
    frac = np.array(list(fractional_position), dtype=float)
    cart = frac @ out.cell
    out.symbols.append(symbol)
    out.positions = np.vstack([out.positions, cart])
    out.comment = f"{structure.comment}; added {symbol} at {label} fractional {frac.tolist()}"
    return out


def fractional_positions(structure: Structure) -> np.ndarray:
    return np.linalg.solve(structure.cell.T, structure.positions.T).T


def write_xyz(structure: Structure, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [str(len(structure.symbols)), structure.comment or "Generated structure"]
    for symbol, pos in zip(structure.symbols, structure.positions):
        lines.append(f"{symbol:2s} {pos[0]: .8f} {pos[1]: .8f} {pos[2]: .8f}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_cif(structure: Structure, path: str | Path, data_name: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    a, b, c = (np.linalg.norm(vector) for vector in structure.cell)
    frac = fractional_positions(structure)
    lines = [
        f"data_{data_name}",
        "_symmetry_space_group_name_H-M 'P 1'",
        "_symmetry_Int_Tables_number 1",
        f"_cell_length_a {a:.8f}",
        f"_cell_length_b {b:.8f}",
        f"_cell_length_c {c:.8f}",
        "_cell_angle_alpha 90",
        "_cell_angle_beta 90",
        "_cell_angle_gamma 90",
        "loop_",
        "_atom_site_label",
        "_atom_site_type_symbol",
        "_atom_site_fract_x",
        "_atom_site_fract_y",
        "_atom_site_fract_z",
    ]
    counts: dict[str, int] = {}
    for symbol, fpos in zip(structure.symbols, frac):
        counts[symbol] = counts.get(symbol, 0) + 1
        wrapped = fpos % 1.0
        lines.append(f"{symbol}{counts[symbol]} {symbol} {wrapped[0]:.8f} {wrapped[1]:.8f} {wrapped[2]:.8f}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def qe_atomic_species(symbols: Iterable[str]) -> str:
    masses = {"Ti": 47.867, "Fe": 55.845, "H": 1.008}
    pseudos = {
        "Ti": "Ti.pbe-spn-kjpaw_psl.1.0.0.UPF",
        "Fe": "Fe.pbe-spn-kjpaw_psl.1.0.0.UPF",
        "H": "H.pbe-kjpaw_psl.1.0.0.UPF",
    }
    ordered = [symbol for symbol in ["Ti", "Fe", "H"] if symbol in set(symbols)]
    return "\n".join(f"{symbol} {masses[symbol]:.6f} {pseudos[symbol]}" for symbol in ordered)


def write_qe_input(
    structure: Structure,
    path: str | Path,
    calculation: str,
    prefix: str,
    ecutwfc: int = 50,
    kpoints: tuple[int, int, int] = (6, 6, 6),
    relax_cell: bool = False,
    nspin: int = 2,
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    nat = len(structure.symbols)
    ntyp = len(set(structure.symbols))
    calc = "vc-relax" if relax_cell else calculation
    occupations = "smearing"
    smearing = "mv"
    degauss = 0.02
    lines = [
        "&CONTROL",
        f"  calculation = '{calc}'",
        f"  prefix = '{prefix}'",
        "  outdir = './tmp'",
        "  pseudo_dir = './pseudo'",
        "  tprnfor = .true.",
        "  tstress = .true.",
        "/",
        "&SYSTEM",
        "  ibrav = 0",
        f"  nat = {nat}",
        f"  ntyp = {ntyp}",
        f"  ecutwfc = {ecutwfc}",
        f"  occupations = '{occupations}'",
        f"  smearing = '{smearing}'",
        f"  degauss = {degauss}",
        f"  nspin = {nspin}",
        "  starting_magnetization(1) = 0.1",
        "  starting_magnetization(2) = 0.3",
        "/",
        "&ELECTRONS",
        "  conv_thr = 1.0d-8",
        "  mixing_beta = 0.4",
        "/",
    ]
    if calc in {"relax", "vc-relax"}:
        lines += [
            "&IONS",
            "  ion_dynamics = 'bfgs'",
            "/",
        ]
    if calc == "vc-relax":
        lines += [
            "&CELL",
            "  cell_dynamics = 'bfgs'",
            "  press_conv_thr = 0.5",
            "/",
        ]
    lines += [
        "ATOMIC_SPECIES",
        qe_atomic_species(structure.symbols),
        "CELL_PARAMETERS angstrom",
    ]
    for vector in structure.cell:
        lines.append(f"  {vector[0]: .10f} {vector[1]: .10f} {vector[2]: .10f}")
    lines.append("ATOMIC_POSITIONS angstrom")
    for symbol, pos in zip(structure.symbols, structure.positions):
        lines.append(f"  {symbol:2s} {pos[0]: .10f} {pos[1]: .10f} {pos[2]: .10f}")
    lines += [
        "K_POINTS automatic",
        f"  {kpoints[0]} {kpoints[1]} {kpoints[2]} 0 0 0",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def nearest_distances(structure: Structure, atom_index: int, symbol: str, n: int = 4) -> list[float]:
    target = structure.positions[atom_index]
    distances = []
    for other_symbol, pos in zip(structure.symbols, structure.positions):
        if other_symbol != symbol:
            continue
        delta = minimum_image_delta(target - pos, structure.cell)
        distances.append(float(np.linalg.norm(delta)))
    return sorted(distances)[:n]


def minimum_image_delta(delta: np.ndarray, cell: np.ndarray) -> np.ndarray:
    frac = np.linalg.solve(cell.T, delta.T).T
    frac -= np.round(frac)
    return frac @ cell
