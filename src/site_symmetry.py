"""Find equivalent H starting sites under symmetries of the cubic TiFe framework."""
from __future__ import annotations

import ast
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_sites(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "HYDROGEN_SITES" for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise ValueError("HYDROGEN_SITES not found")


def pristine_framework(path):
    text = Path(path).read_text(encoding="utf-8")
    lines = text.split("CELL_PARAMETERS angstrom\n", 1)[1].split("ATOMIC_POSITIONS", 1)[0].strip().splitlines()
    matrix = [list(map(float, line.split())) for line in lines[:3]]
    side = matrix[0][0]
    if side <= 0 or any(
        abs(matrix[i][j] - (side if i == j else 0)) > 1e-6
        for i in range(3) for j in range(3)
    ):
        raise ValueError("Axis-permutation test requires an aligned cubic cell")
    positions = text.split("ATOMIC_POSITIONS angstrom\n", 1)[1].split("K_POINTS", 1)[0].strip().splitlines()
    return [(words[0], tuple(round((float(x) / side) % 1, 7) for x in words[1:4]))
            for words in (line.split() for line in positions)]


def allowed_permutations(framework):
    original = sorted(framework)
    return [axes for axes in itertools.permutations(range(3))
            if sorted((symbol, tuple(pos[i] for i in axes))
                      for symbol, pos in framework) == original]


def group_sites(sites, allowed):
    if not allowed:
        raise ValueError("No permitted axis symmetries")
    groups = {}
    for name, site in sites.items():
        key = min(tuple(round(float(site[i]) % 1, 7) for i in axes) for axes in allowed)
        groups.setdefault(key, []).append(name)
    return list(groups.values())


def analyze(site_path, pristine_path):
    sites = read_sites(site_path)
    allowed = allowed_permutations(pristine_framework(pristine_path))
    groups = group_sites(sites, allowed)
    return {
        "candidates": len(sites), "unique_starting_sites": len(groups),
        "planned_relaxations_avoided": len(sites) - len(groups),
        "planned_run_reduction_percent": round(100 * (1 - len(groups)/len(sites)), 2),
        "representatives": [group[0] for group in groups],
        "equivalent_groups": groups,
        "allowed_axis_permutations": len(allowed),
        "scope": "Ideal unrelaxed cubic B2 supercell. Does not model magnetic symmetry breaking, defects, relaxation, or energies.",
    }


def write_report(result, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "site_symmetry.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# TiFe hydrogen: cubic site screening", "",
        f"Starting positions: {result['candidates']}.",
        f"Distinct positions: {result['unique_starting_sites']}.",
        f"Duplicated positions: {result['planned_relaxations_avoided']}.",
        f"Potential reduction in scheduled site relaxations: {result['planned_run_reduction_percent']}%.",
        "", "Equivalent groups:",
    ]
    lines += ["- " + ", ".join(group) for group in result["equivalent_groups"]]
    lines += ["", result["scope"], "",
              "Planned run reduction is not measured CPU savings and does not establish site stability.", ""]
    (directory / "site_symmetry.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    report = analyze(ROOT / "src/add_hydrogen.py", ROOT / "qe_inputs/pristine/Ti8Fe8_relax.in")
    write_report(report, ROOT / "results/preflight")
    print(json.dumps(report, indent=2))
