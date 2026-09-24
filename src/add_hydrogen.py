from pathlib import Path

from build_supercell import build_tife_supercell
from structure_io import add_atom, write_cif, write_qe_input, write_xyz


ROOT = Path(__file__).resolve().parents[1]

# Candidate positions are fractional coordinates of the 2x2x2 supercell.
# They are starting points for relaxation, not final site assignments.
HYDROGEN_SITES = {
    "Site_A_Ti_rich_octahedral": (0.25, 0.25, 0.00),
    "Site_B_mixed_octahedral": (0.25, 0.00, 0.25),
    "Site_C_tetrahedral_like": (0.125, 0.125, 0.125),
}

SITE_FILE_TAGS = {
    "Site_A_Ti_rich_octahedral": "siteA",
    "Site_B_mixed_octahedral": "siteB",
    "Site_C_tetrahedral_like": "siteC",
}


def main() -> None:
    supercell = build_tife_supercell()
    for label, frac in HYDROGEN_SITES.items():
        tag = SITE_FILE_TAGS[label]
        structure = add_atom(supercell, "H", frac, label)
        write_cif(structure, ROOT / "structures" / f"Ti8Fe8H_{tag}.cif", f"Ti8Fe8H_{tag}")
        write_xyz(structure, ROOT / "structures" / f"Ti8Fe8H_{tag}.xyz")
        write_qe_input(
            structure,
            ROOT / "qe_inputs" / "hydrogen_sites" / f"Ti8Fe8H_{tag}_relax.in",
            calculation="relax",
            prefix=f"Ti8Fe8H_{tag}",
            ecutwfc=50,
            kpoints=(4, 4, 4),
        )


if __name__ == "__main__":
    main()
