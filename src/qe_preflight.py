"""Check Quantum ESPRESSO input consistency before expensive calculations."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def setting(text, key):
    match = re.search(r"(?m)^\s*" + re.escape(key) + r"\s*=\s*([^!\n,]+)", text)
    return match.group(1).strip().strip("',\" ") if match else None


def rows_between(text, start, stop):
    match = re.search(r"(?m)^" + re.escape(start) + r"[^\n]*\n(.*?)(?=^" + re.escape(stop) + r"|\Z)", text, re.S | re.M)
    return [line.strip() for line in match.group(1).splitlines() if line.strip()] if match else []


def inspect_input(path):
    content = Path(path).read_text(encoding="utf-8")
    errors = []
    warnings = []
    if "&DOS" in content and "&CONTROL" not in content:
        return {"file": str(path), "kind": "dos.x", "errors": [], "warnings": []}
    for card in ("&CONTROL", "&SYSTEM", "&ELECTRONS", "ATOMIC_SPECIES",
                 "CELL_PARAMETERS", "ATOMIC_POSITIONS", "K_POINTS"):
        if card not in content:
            errors.append("missing " + card)
    if errors:
        return {"file": str(path), "kind": "pw.x", "errors": errors, "warnings": warnings}
    try:
        nat = int(setting(content, "nat") or "")
        ntyp = int(setting(content, "ntyp") or "")
        cutoff = float(setting(content, "ecutwfc") or "")
        nspin = int(setting(content, "nspin") or "1")
    except ValueError:
        return {"file": str(path), "kind": "pw.x",
                "errors": ["invalid nat, ntyp, ecutwfc or nspin"], "warnings": warnings}
    species = rows_between(content, "ATOMIC_SPECIES", "CELL_PARAMETERS")
    atoms = rows_between(content, "ATOMIC_POSITIONS", "K_POINTS")
    if len(species) != ntyp:
        errors.append(f"ntyp={ntyp} but {len(species)} species listed")
    if len(atoms) != nat:
        errors.append(f"nat={nat} but {len(atoms)} positions listed")
    if cutoff <= 0:
        errors.append("ecutwfc must be positive")
    mag_idx = [int(x) for x in re.findall(r"starting_magnetization\s*\(\s*(\d+)\s*\)", content)]
    if mag_idx and nspin != 2:
        errors.append("starting_magnetization requires nspin=2")
    if any(i < 1 or i > ntyp for i in mag_idx):
        errors.append(f"starting_magnetization index exceeds ntyp={ntyp}")
    kgrid = re.search(r"K_POINTS\s+automatic\s*\n\s*(\d+)\s+(\d+)\s+(\d+)\s+([01])\s+([01])\s+([01])", content)
    if "K_POINTS automatic" in content and (
        not kgrid or min(int(value) for value in kgrid.groups()[:3]) < 1
    ):
        errors.append("invalid automatic k-point mesh")
    if nspin == 1 and setting(content, "occupations") == "smearing":
        warnings.append("non-spin-polarized input uses smearing; check molecular reference")
    return {"file": str(path), "kind": "pw.x", "nat": nat, "ntyp": ntyp,
            "ecutwfc_Ry": cutoff, "errors": errors, "warnings": warnings}


def scan(root):
    inputs = sorted(Path(root).glob("**/*.in"))
    if not inputs:
        raise ValueError(f"No Quantum ESPRESSO input files under {root}")
    files = [inspect_input(path) for path in inputs]
    return {
        "inputs": len(files),
        "pw_inputs": sum(f["kind"] == "pw.x" for f in files),
        "failed_inputs": sum(bool(f["errors"]) for f in files),
        "warnings": sum(len(f["warnings"]) for f in files),
        "files": files,
        "scope": "Input consistency only; no pseudopotential or DFT executable check and no converged energies.",
    }


def write_report(audit, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "qe_preflight.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# TiFe DFT input checks", "",
        f"Files checked: {audit['inputs']} ({audit['pw_inputs']} pw.x inputs).",
        f"Inputs with errors: {audit['failed_inputs']}.",
        f"Warnings: {audit['warnings']}.",
        "",
        "| File | Errors | Warnings |", "|---|---|---|",
    ]
    for file in audit["files"]:
        lines.append(f"| {Path(file['file']).name} | {'; '.join(file['errors']) or 'none'} | {'; '.join(file['warnings']) or 'none'} |")
    lines += ["", "## Limits", "", audit["scope"],
              "Hydrogen insertion energies remain uncalculated until the actual QE runs and convergence checks are complete.",
              "", "QE reference: https://www.quantum-espresso.org/Doc/INPUT_PW.html", ""]
    (output / "qe_preflight.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, default=Path("qe_inputs"))
    parser.add_argument("--output", type=Path, default=Path("results/preflight"))
    args = parser.parse_args()
    result = scan(args.inputs)
    write_report(result, args.output)
    print(json.dumps({key: value for key, value in result.items() if key != "files"}, indent=2))
    if result["failed_inputs"]:
        raise SystemExit(1)
