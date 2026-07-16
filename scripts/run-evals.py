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
VO = ROOT / "scripts" / "validate-output.py"

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


def vo_run(deliverable: str, lock: str) -> tuple[int, str]:
    return _run([str(VO), str(EX / deliverable), "--lock", str(EX / lock), "--json"])


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
    "worked-creative-production.json": "ship",
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

# ---- v1.0.0: creative-production gates (Pillar 1 brief, Pillar 2 options, Pillar 3 output audit,
# Pillar 4 model routing) — negatives built off the new creative-production golden ----
cp_base = load("worked-creative-production.json")

d = copy.deepcopy(cp_base); del d["brief"]["hardNos"]; d["brief"]["handoffPageRead"] = False
rc, out = vr_obj(d)
check(
    "reject: incomplete brief batches every missing field in one failure",
    rc == 1 and "brief incomplete" in out.lower() and "hardnos" in out.lower() and "handoffpageread" in out.lower(),
)

d = copy.deepcopy(cp_base); d["options"] = d["options"][:1]
rc, out = vr_obj(d); check("reject: fewer than 2 options for creative generation", rc == 1 and "2-3 options" in out.lower())

d = copy.deepcopy(cp_base); d["options"].append(copy.deepcopy(d["options"][0]))
rc, out = vr_obj(d); check("reject: more than 3 options for creative generation", rc == 1 and "2-3 options" in out.lower())

d = copy.deepcopy(cp_base); d["options"][1]["lockCompliant"] = False
rc, out = vr_obj(d); check("reject: a presented option that is not lock-compliant", rc == 1 and "lockcompliant" in out.lower())

d = copy.deepcopy(cp_base); d["options"][1]["distinctionAxis"] = d["options"][0]["distinctionAxis"]
rc, out = vr_obj(d); check("reject: options are not actually distinct", rc == 1 and "distinct" in out.lower())

d = copy.deepcopy(cp_base); d["outputAudit"]["pass"] = False
rc, out = vr_obj(d); check("reject: ship verdict with a failing output audit", rc == 1 and "outputaudit" in out.lower())

d = copy.deepcopy(cp_base); del d["outputAudit"]
rc, out = vr_obj(d); check("reject: ship verdict with no output audit at all", rc == 1 and "outputaudit" in out.lower())

d = copy.deepcopy(cp_base); d["trace"][0]["modelTier"] = "deep"
rc, out = vr_obj(d); check("reject: gate step (brief-gate) not tagged fast", rc == 1 and "fast" in out.lower())

d = copy.deepcopy(cp_base); d["trace"][0]["modelTier"] = "leisurely"
rc, out = vr_obj(d); check("reject: unknown modelTier value", rc == 1 and "modeltier" in out.lower())

# ---- output audit (scripts/validate-output.py) smoke tests ----
rc, out = vo_run("deliverable-pass.html", "lock-fixture.json")
check("output-audit: in-lock, no-Hard-NO deliverable passes", rc == 0 and json.loads(out)["pass"] is True)

rc, out = vo_run("deliverable-fail.html", "lock-fixture.json")
obj = json.loads(out) if out.strip().startswith("{") else {}
check("output-audit: out-of-lock color caught", rc == 1 and "#111111" in obj.get("colorsOutOfLock", []))
check(
    "output-audit: both Hard-NO patterns caught",
    set(obj.get("hardNoHits", [])) == {"lorem ipsum", "click here"},
)

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
