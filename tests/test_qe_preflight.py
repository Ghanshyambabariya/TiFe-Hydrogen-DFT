from pathlib import Path
import runpy

CODE = runpy.run_path(str(Path(__file__).resolve().parents[1] / "src" / "qe_preflight.py"))

BAD = """&CONTROL
 calculation = 'scf'
/
&SYSTEM
 nat=2
 ntyp=1
 ecutwfc=50
 nspin=1
 starting_magnetization(1)=0.1
 starting_magnetization(2)=0.3
/
&ELECTRONS
/
ATOMIC_SPECIES
H 1.008 H.upf
CELL_PARAMETERS angstrom
15 0 0
0 15 0
0 0 15
ATOMIC_POSITIONS angstrom
H 0 0 0
H 0 0 0.74
K_POINTS automatic
1 1 1 0 0 0
"""


def test_bad_hydrogen_reference_is_flagged(tmp_path):
    p = tmp_path / "h2.in"
    p.write_text(BAD)
    assert len(CODE["inspect_input"](p)["errors"]) == 2


def test_corrected_hydrogen_reference(tmp_path):
    p = tmp_path / "h2.in"
    p.write_text(BAD.replace(" starting_magnetization(1)=0.1\n", "").replace(" starting_magnetization(2)=0.3\n", ""))
    assert CODE["inspect_input"](p)["errors"] == []
    report = CODE["scan"](tmp_path)
    CODE["write_report"](report, tmp_path / "result")
    assert report["failed_inputs"] == 0
    assert (tmp_path / "result" / "qe_preflight.md").exists()


def test_repository_inputs_pass():
    repo = Path(__file__).resolve().parents[1]
    report = CODE["scan"](repo / "qe_inputs")
    assert report["inputs"] == 17
    assert report["failed_inputs"] == 0
