#!/usr/bin/env python3
"""revüe eval suite.

Proves the skill's guarantees with the shipped validators, on every push:
  - golden reviews across modes validate AND reach the expected verdict;
  - every failure mode (dead-end verdict, false ship, thin evidence, no source, no
    freshness, bad path owner) is correctly rejected;
  - the bugs we fixed stay fixed (plural "screenshots" accepted; "ship with changes"
    is not misread as "ship").

Exits non-zero if any expectation is unmet. Stdlib only.
"""

from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EX = ROOT / "examples"
VR = ROOT / "scripts" / "validate-run.py"
VE = ROOT / "scripts" / "validate-evidence.py"

cases: list[tuple[str, bool]] = []


def check(desc: str, ok: bool) -> None:
    cases.append((desc, ok))


def _run(args: list[str]) -> tuple[int, str]:
    p = subprocess.run([sys.executable, *args], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def vr_file(name: str) -> tuple[int, str]:
    return _run([str(VR), str(EX / name), "--strict"])


def vr_obj(obj: dict) -> tuple[int, str]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(obj, f)
        path = f.name
    return _run([str(VR), path, "--strict"])


def ve_file(path: Path, extra: list[str]) -> tuple[int, str]:
    return _run([str(VE), str(path), "--strict", *extra])


def load(name: str) -> dict:
    return json.loads((EX / name).read_text(encoding="utf-8"))


def md_verdict(path: Path) -> str:
    m = re.search(r"Verdict:\s*(ship with changes|ship|caution|block)", path.read_text(encoding="utf-8"), re.I)
    return m.group(1).lower() if m else "none"


# ---- golden JSON run artifacts: validate + expected verdict ----
GOLDEN_JSON = {
    "sample-run-vip-lake-travis.json": "caution",
    "worked-converge-vip.json": "caution",
    "worked-product-shaping.json": "caution",
    "worked-client-delivery.json": "ship with changes",
}
for name, expected in GOLDEN_JSON.items():
    rc, _ = vr_file(name)
    check(f"golden {name} validates (strict)", rc == 0)
    check(f"golden {name} verdict == {expected}", load(name)["verdict"]["value"] == expected)

# ---- golden Markdown handoffs: validate + expected verdict ----
GOLDEN_MD = {
    "worked-design-handoff.md": (["--mode", "design-handoff"], "caution"),
    "worked-implementation-review.md": ([], "ship with changes"),
}
for name, (extra, expected) in GOLDEN_MD.items():
    rc, _ = ve_file(EX / name, extra)
    check(f"golden {name} validates (strict)", rc == 0)
    check(f"golden {name} verdict == {expected}", md_verdict(EX / name) == expected)

# ---- negatives: every failure mode must be rejected, for the right reason ----
base = load("worked-converge-vip.json")

d = copy.deepcopy(base); d.pop("pathToShip", None); d.pop("decisionsNeeded", None)
rc, out = vr_obj(d); check("reject: non-ship verdict with no path to ship", rc == 1 and "path" in out.lower())

d = copy.deepcopy(base); d["verdict"]["value"] = "ship"
rc, out = vr_obj(d); check("reject: ship over a failing scorecard", rc == 1 and "ship verdict" in out.lower())

d = copy.deepcopy(base); d["evidence"] = d["evidence"][:2]
rc, out = vr_obj(d); check("reject: evidence below the floor", rc == 1 and "floor" in out.lower())

d = copy.deepcopy(base)
d["evidence"] = [
    {"category": "result", "statement": "seen a thing"},
    {"category": "result", "statement": "seen another"},
    {"category": "limitation", "statement": "did not check X"},
]
rc, out = vr_obj(d); check("reject: no source-category evidence", rc == 1 and "source" in out.lower())

d = copy.deepcopy(base)
for e in d["evidence"]:
    e["statement"] = re.sub(r"(inspected|screenshot|this session|captured|observed|snapshot|verified|as of|today|live|dated|run at|exit code|output)", "seen", e["statement"], flags=re.I)
rc, out = vr_obj(d); check("reject: evidence with no freshness marker", rc == 1 and "recency" in out.lower())

d = copy.deepcopy(base); d["pathToShip"][0]["owner"] = "robot"
rc, out = vr_obj(d); check("reject: path-to-ship item with a bad owner", rc == 1 and "owner" in out.lower())

# ---- regression guards: the bugs we fixed must stay fixed ----
design = (EX / "worked-design-handoff.md").read_text(encoding="utf-8")
plural = design.replace("screenshot (1512x785 capture)", "screenshots captured")
with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
    f.write(plural); ppath = f.name
rc, _ = _run([str(VE), ppath, "--mode", "design-handoff", "--strict"])
check("regression: plural 'screenshots' accepted", rc == 0)

# "ship with changes" must not be misread as "ship" (the impl golden is 'ship with changes' and passes)
rc, _ = ve_file(EX / "worked-implementation-review.md", [])
check("regression: 'ship with changes' not misread as 'ship'", rc == 0)


def main() -> int:
    passed = sum(1 for _, ok in cases if ok)
    for desc, ok in cases:
        print(f"[{'ok  ' if ok else 'FAIL'}] {desc}")
    print(f"\n{passed}/{len(cases)} eval cases passed")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
