from pathlib import Path

from structure_io import b2_tife, write_cif, write_qe_input, write_xyz


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    structure = b2_tife(a=2.97)
    write_cif(structure, ROOT / "structures" / "TiFe.cif", "B2_TiFe")
    write_xyz(structure, ROOT / "structures" / "TiFe.xyz")
    write_qe_input(
        structure,
        ROOT / "qe_inputs" / "pristine" / "TiFe_vc_relax.in",
        calculation="vc-relax",
        prefix="TiFe_pristine",
        ecutwfc=50,
        kpoints=(8, 8, 8),
        relax_cell=True,
    )


if __name__ == "__main__":
    main()
