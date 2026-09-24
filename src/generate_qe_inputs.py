from pathlib import Path

import numpy as np

from add_hydrogen import HYDROGEN_SITES
from build_supercell import build_tife_supercell
from structure_io import Structure, b2_tife, write_qe_input


ROOT = Path(__file__).resolve().parents[1]


def write_convergence_inputs() -> None:
    primitive = b2_tife(a=2.97)
    for ecut in [30, 40, 50, 60]:
        write_qe_input(
            primitive,
            ROOT / "qe_inputs" / "convergence" / f"TiFe_ecut_{ecut}Ry.in",
            calculation="scf",
            prefix=f"TiFe_ecut_{ecut}",
            ecutwfc=ecut,
            kpoints=(6, 6, 6),
        )
    for mesh in [(4, 4, 4), (6, 6, 6), (8, 8, 8)]:
        label = "x".join(map(str, mesh))
        write_qe_input(
            primitive,
            ROOT / "qe_inputs" / "convergence" / f"TiFe_k_{label}.in",
            calculation="scf",
            prefix=f"TiFe_k_{label}",
            ecutwfc=50,
            kpoints=mesh,
        )


def write_h2_input() -> None:
    cell = np.eye(3) * 15.0
    positions = np.array([[7.5, 7.5, 7.13], [7.5, 7.5, 7.87]])
    h2 = Structure(["H", "H"], positions, cell, "Isolated H2 molecule in a large cubic cell")
    write_qe_input(
        h2,
        ROOT / "qe_inputs" / "h2" / "H2_scf.in",
        calculation="scf",
        prefix="H2_reference",
        ecutwfc=50,
        kpoints=(1, 1, 1),
        nspin=1,
    )


def write_dos_inputs() -> None:
    primitive = b2_tife(a=2.97)
    supercell = build_tife_supercell()
    write_qe_input(
        primitive,
        ROOT / "qe_inputs" / "dos" / "TiFe_scf_for_dos.in",
        calculation="scf",
        prefix="TiFe_dos",
        ecutwfc=50,
        kpoints=(10, 10, 10),
    )
    write_qe_input(
        supercell,
        ROOT / "qe_inputs" / "dos" / "Ti8Fe8_scf_for_dos.in",
        calculation="scf",
        prefix="Ti8Fe8_dos",
        ecutwfc=50,
        kpoints=(6, 6, 6),
    )
    dos_template = """&DOS
  prefix = '{prefix}'
  outdir = './tmp'
  fildos = '{filename}'
  Emin = -12.0
  Emax = 8.0
  DeltaE = 0.02
/
"""
    (ROOT / "qe_inputs" / "dos" / "TiFe_dos.in").write_text(
        dos_template.format(prefix="TiFe_dos", filename="TiFe.dos"), encoding="utf-8"
    )
    (ROOT / "qe_inputs" / "dos" / "Ti8Fe8_dos.in").write_text(
        dos_template.format(prefix="Ti8Fe8_dos", filename="Ti8Fe8.dos"), encoding="utf-8"
    )


def main() -> None:
    write_convergence_inputs()
    write_h2_input()
    write_dos_inputs()
    # Ensure hydrogen input folder exists even before add_hydrogen.py is run.
    for site in HYDROGEN_SITES:
        _ = site
    (ROOT / "qe_inputs" / "hydrogen_sites").mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()
