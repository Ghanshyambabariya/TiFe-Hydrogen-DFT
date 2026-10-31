from pathlib import Path
import itertools
import runpy

CODE = runpy.run_path(str(Path(__file__).resolve().parents[1] / "src/site_symmetry.py"))


def test_axis_permutation_groups():
    sites = {"A": (0.25, 0.25, 0), "B": (0.25, 0, 0.25), "C": (0.125, 0.125, 0.125)}
    assert CODE["group_sites"](sites, list(itertools.permutations(range(3)))) == [["A", "B"], ["C"]]


def test_real_tife_framework():
    root = Path(__file__).resolve().parents[1]
    result = CODE["analyze"](root / "src/add_hydrogen.py", root / "qe_inputs/pristine/Ti8Fe8_relax.in")
    assert result["candidates"] == 3
    assert result["unique_starting_sites"] == 2
    assert result["planned_relaxations_avoided"] == 1
    assert result["allowed_axis_permutations"] == 6
