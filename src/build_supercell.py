from pathlib import Path

from structure_io import b2_tife, make_supercell, write_cif, write_qe_input, write_xyz


ROOT = Path(__file__).resolve().parents[1]


def build_tife_supercell():
    return make_supercell(b2_tife(a=2.97), repeats=(2, 2, 2))


def main() -> None:
    supercell = build_tife_supercell()
    write_cif(supercell, ROOT / "structures" / "Ti8Fe8.cif", "Ti8Fe8")
    write_xyz(supercell, ROOT / "structures" / "Ti8Fe8.xyz")
    write_qe_input(
        supercell,
        ROOT / "qe_inputs" / "pristine" / "Ti8Fe8_relax.in",
        calculation="relax",
        prefix="Ti8Fe8_pristine",
        ecutwfc=50,
        kpoints=(4, 4, 4),
    )


if __name__ == "__main__":
    main()
