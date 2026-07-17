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
VC = ROOT / "scripts" / "validate-conformance.py"

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
    "worked-premium-production.json": "ship",
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

# ---- v1.0.0 red team: deliverables that actively try to sneak past the output audit ----
# Every fixture below is an attack on scripts/validate-output.py. Each must be REJECTED (rc == 1)
# for the specific reason the attack targets — not incidentally.

def vo_audit(deliverable: str) -> tuple[int, dict]:
    rc, out = vo_run(deliverable, "lock-fixture.json")
    try:
        return rc, json.loads(out)
    except json.JSONDecodeError:
        return rc, {}

# The exact original failure this version exists to prevent: a generic template-clone landing page
# with guessed off-palette colors, an off-brand template font, generic link text, and a fabricated
# "4.9 / 200+" metric — the deliverable that previously shipped undetected.
rc, a = vo_audit("redteam-original-failure.html")
check("red team: original failure — generic clone REJECTED", rc == 1 and a.get("pass") is False)
check(
    "red team: original failure — guessed template colors caught",
    "#1a73e8" in a.get("colorsOutOfLock", []) and "#34a853" in a.get("colorsOutOfLock", []),
)
check(
    "red team: original failure — fabricated 4.9 / 200+ metric caught",
    any("4.9" in c for c in a.get("unverifiedClaims", []))
    and any("200+" in c for c in a.get("unverifiedClaims", [])),
)
check("red team: original failure — off-brand template font caught", "Inter" in a.get("fontsOutOfLock", []))
check("red team: original failure — generic 'click here' caught", "click here" in a.get("hardNoHits", []))

rc, a = vo_audit("redteam-css-variable-color.html")
check(
    "red team: named color behind a CSS variable REJECTED",
    rc == 1 and "#663399" in a.get("colorsOutOfLock", []),
)

rc, a = vo_audit("redteam-hsl-near-miss.html")
check(
    "red team: hsl()/modern-rgb near-miss shades REJECTED and labeled",
    rc == 1
    and set(a.get("nearMisses", {}).values()) == {"#062456", "#ff5747"},
)

rc, a = vo_audit("redteam-attr-and-datauri.html")
check(
    "red team: hash-less attribute hex REJECTED",
    rc == 1 and {"#112233", "#445566"} <= set(a.get("colorsOutOfLock", [])),
)
check(
    "red team: off-palette color inside base64 SVG data URI caught",
    "#e91e63" in a.get("colorsOutOfLock", []),
)
check("red team: Hard NO delivered via atob() caught", "click here" in a.get("hardNoHits", []))

rc, a = vo_audit("redteam-external-styles.html")
check(
    "red team: colors hidden in an external stylesheet — unverifiable, REJECTED",
    rc == 1 and any("external stylesheet" in u for u in a.get("unverifiable", [])),
)

rc, a = vo_audit("redteam-fabricated-metric.html")
check(
    "red team: on-palette page with only a fabricated metric REJECTED",
    rc == 1 and not a.get("colorsOutOfLock") and len(a.get("unverifiedClaims", [])) >= 2,
)

rc, a = vo_audit("redteam-offlock-font.html")
check(
    "red team: on-palette page with an off-lock font REJECTED",
    rc == 1 and "Playfair Display" in a.get("fontsOutOfLock", []),
)

rc, a = vo_audit("redteam-obfuscated-hardno.html")
check(
    "red team: homoglyph/zero-width/entity/tag-split Hard NOs all caught",
    rc == 1 and set(a.get("hardNoHits", [])) == {"lorem ipsum", "click here"},
)

# An approved claim in the lock's allowlist must still pass — the metric gate is a gate, not a ban.
_claims_lock = json.loads((EX / "lock-fixture.json").read_text(encoding="utf-8"))
_claims_lock["claims"] = ["4.8 / 5 rating from 132 reviews"]
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump(_claims_lock, f); _claims_lock_path = f.name
with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
    f.write(
        "<style>body{background:#062456;color:#FFFFFF;font-family:Quicksand,Arial,sans-serif}</style>"
        "<h1>Reserve Your Boat</h1><p>4.8 / 5 rating from 132 reviews</p>"
    ); _claims_html_path = f.name
rc, out = _run([str(VO), _claims_html_path, "--lock", _claims_lock_path, "--json"])
check("red team control: lock-approved metric claim still passes", rc == 0 and json.loads(out)["pass"] is True)

# ---- v1.0.0 red team: runs that try to sneak past validate-run's creative gates ----
d = copy.deepcopy(cp_base); d["produces"] = "review"
rc, out = vr_obj(d)
check(
    "red team: creative run undeclared as creative-production REJECTED",
    rc == 1 and "declare the run" in out.lower(),
)

d = copy.deepcopy(cp_base)
d["outputAudit"]["pass"] = True
d["outputAudit"]["colorsOutOfLock"] = ["#1a73e8"]
rc, out = vr_obj(d)
check(
    "red team: forged outputAudit (pass flipped true over listed violations) REJECTED",
    rc == 1 and "internally inconsistent" in out.lower(),
)

d = copy.deepcopy(cp_base)
d["options"][1]["distinctionAxis"] = d["options"][0]["distinctionAxis"].upper().replace(".", "!")
rc, out = vr_obj(d)
check(
    "red team: paraphrased duplicate distinctionAxis (case/punctuation) REJECTED",
    rc == 1 and "distinct" in out.lower(),
)

d = copy.deepcopy(cp_base); d["brief"]["handoffPageRead"] = "yes"
rc, out = vr_obj(d)
check(
    "red team: handoffPageRead as string 'yes' (not boolean true) REJECTED",
    rc == 1 and "handoffpageread" in out.lower(),
)

# ---- v1.0.0 dogfood: the pipeline run on revüe's own brand stays reproducible ----
DOG = EX / "dogfood"
rc, out = _run([str(VR), str(DOG / "run-incomplete-brief.json"), "--strict"])
check(
    "dogfood: incomplete brief blocked with one batched field request",
    rc == 1 and out.lower().count("brief incomplete") == 1 and "handoffpageread" in out.lower(),
)
rc, out = _run([str(VO), str(DOG / "winner-draft-1.html"), "--lock", str(DOG / "revue-lock.json")])
check(
    "dogfood: draft with guessed hover shade rejected as near-miss",
    rc == 1 and "#e64435" in out and "near-miss" in out,
)
rc, _ = _run([str(VO), str(DOG / "winner.html"), "--lock", str(DOG / "revue-lock.json")])
check("dogfood: audited winner passes clean", rc == 0)
rc, _ = _run([str(VR), str(DOG / "run.json"), "--strict"])
check("dogfood: full run artifact validates (strict)", rc == 0)
check(
    "dogfood: verdict is 'ship with changes' (no browser preview, no ship)",
    json.loads((DOG / "run.json").read_text(encoding="utf-8"))["verdict"]["value"] == "ship with changes",
)

# ---- v1.1.0: tier gate (Standard/Premium/Custom), elevate, and brief-conformance ----
prem_base = load("worked-premium-production.json")

d = copy.deepcopy(prem_base); del d["brief"]["tier"]
rc, out = vr_obj(d)
check("reject: brief missing tier batches into the incomplete-brief failure", rc == 1 and "tier" in out.lower())

d = copy.deepcopy(prem_base); d["brief"]["tier"] = "Enterprise"
rc, out = vr_obj(d)
check("reject: brief.tier must be one of Standard/Premium/Custom", rc == 1 and "tier" in out.lower())

d = copy.deepcopy(prem_base); d["outputAudit"]["elevatePass"] = False
rc, out = vr_obj(d)
check(
    "reject: Premium ship requires elevatePass — meets only the Standard bar",
    rc == 1 and "elevatepass" in out.lower() and "standard bar" in out.lower(),
)

d = copy.deepcopy(prem_base); del d["outputAudit"]["elevateChecks"]; del d["outputAudit"]["elevatePass"]
rc, out = vr_obj(d)
check("reject: Premium ship with no elevate checks run at all", rc == 1 and "elevatepass" in out.lower())

d = copy.deepcopy(prem_base); d["brief"]["tier"] = "Custom"; d["trace"][1]["modelTier"] = "standard"
rc, out = vr_obj(d)
check(
    "reject: Custom tier ship with no tierSignoff",
    rc == 1 and "tiersignoff" in out.lower(),
)

d = copy.deepcopy(prem_base); d["trace"][1]["modelTier"] = "standard"
rc, out = vr_obj(d)
check(
    "reject: Premium tier options-generation not tagged deep",
    rc == 1 and "options-generation" in out.lower() and "deep" in out.lower(),
)

d = copy.deepcopy(prem_base)
d["conformance"]["pass"] = False
rc, out = vr_obj(d)
check(
    "reject: declared brief.structure but conformance fails",
    rc == 1 and "conformance" in out.lower(),
)

d = copy.deepcopy(prem_base); del d["conformance"]
rc, out = vr_obj(d)
check(
    "reject: declared brief.structure but conformance never ran",
    rc == 1 and "conformance" in out.lower(),
)

# A Custom-tier run WITH a proper human sign-off must be allowed to ship.
d = copy.deepcopy(prem_base)
d["brief"]["tier"] = "Custom"
d["trace"][1]["modelTier"] = "standard"
d["tierSignoff"] = {"by": "Gary Corriston", "note": "approved the bespoke direction directly"}
rc, out = vr_obj(d)
check("accept: Custom tier ship with a proper human tierSignoff", rc == 0)

# ---- v1.1.0: output-audit --tier premium — the elevate heuristics fire correctly ----
rc, out = _run([str(VO), str(EX / "premium-exemplar.html"), "--lock", str(EX / "premium-lock.json"),
                "--tier", "premium", "--json"])
prem_audit = json.loads(out)
check("premium exemplar: base lock/font/Hard-NO audit passes", not prem_audit["colorsOutOfLock"] and not prem_audit["fontsOutOfLock"])
check("premium exemplar: all four elevate checks pass", rc == 0 and prem_audit["elevatePass"] is True)

rc, out = _run([str(VO), str(EX / "deliverable-pass.html"), "--lock", str(EX / "lock-fixture.json"),
                "--tier", "premium", "--json"])
standard_only = json.loads(out)
check(
    "red team: Standard-bar-only deliverable flagged when audited at --tier premium",
    rc == 1 and standard_only["pass"] is False and standard_only["elevatePass"] is False
    and not standard_only["colorsOutOfLock"],  # proves it's the elevate bar failing, not the base lock
)
check(
    "premium heuristic: no hero marker -> full-bleed hero + scrim both fail",
    {c["check"] for c in standard_only["elevateChecks"] if c["status"] == "fail"}
    >= {"full-bleed hero section", "legibility scrim over hero imagery", "sticky action bar"},
)

# Same file at --tier standard (default) is unaffected — no elevate bar was ever asked for.
rc, out = _run([str(VO), str(EX / "deliverable-pass.html"), "--lock", str(EX / "lock-fixture.json"), "--json"])
check("standard tier: same deliverable passes clean with no elevateChecks", rc == 0 and "elevateChecks" not in json.loads(out))

# ---- v1.1.0: brief-conformance (scripts/validate-conformance.py) ----
rc, out = _run([str(VC), str(EX / "conformance-pass.html"), "--structure", str(EX / "structure-fixture.json"), "--json"])
check("conformance: sections present, ordered, no forbidden elements, placeholder intact -> pass", rc == 0 and json.loads(out)["pass"] is True)

rc, out = _run([str(VC), str(EX / "conformance-fail.html"), "--structure", str(EX / "structure-fixture.json"), "--json"])
conf_fail = json.loads(out)
check("conformance: missing section caught", rc == 1 and "proof" in conf_fail["missingSections"])
check("conformance: order violation caught", bool(conf_fail["orderViolations"]))
check("conformance: forbidden element (banned custom header) caught", "class=\"custom-header\"" in conf_fail["forbiddenHits"])
check("conformance: missing required placeholder caught (guessed value instead)", "[CLIENT_PHONE]" in conf_fail["missingPlaceholders"])

rc, out = _run([str(VC), str(EX / "premium-exemplar.html"), "--structure", str(EX / "premium-structure.json"), "--json"])
check("conformance: premium exemplar's real sections conform to its own structure spec", rc == 0 and json.loads(out)["pass"] is True)

# ---- v1.1.0 red team: the three failure classes, plus attacks on the new gates themselves ----

# Failure class 1: a page DECLARED Premium that ships clean-template. Its base audit is clean —
# only the tier bar catches it, and it must catch all four elevate rules.
rc, out = _run([str(VO), str(EX / "redteam-premium-clean-template.html"),
                "--lock", str(EX / "premium-lock.json"), "--tier", "premium", "--json"])
ct = json.loads(out)
check(
    "red team: Premium-declared clean-template FAILS its tier (base audit clean, elevatePass false)",
    rc == 1 and ct["elevatePass"] is False
    and not ct["colorsOutOfLock"] and not ct["fontsOutOfLock"]
    and not ct["hardNoHits"] and not ct["unverifiedClaims"] and not ct["unverifiable"],
)
check(
    "red team: clean-template misses all four elevate rules by name",
    {c["check"] for c in ct["elevateChecks"] if c["status"] == "fail"}
    == {"full-bleed hero section", "legibility scrim over hero imagery",
        "display type system (serif display + sans body)", "sticky action bar"},
)
# ...and a ship verdict carrying that audit must be rejected by the run gate.
d = copy.deepcopy(prem_base)
d["outputAudit"] = {**ct, "deliverablePath": "examples/redteam-premium-clean-template.html"}
rc, out = vr_obj(d)
check(
    "red team: ship over the clean-template Premium audit REJECTED as Standard-bar-only",
    rc == 1 and "standard bar" in out.lower(),
)

# Gaming the elevate heuristics: hidden hero + 1px img + cover/text-shadow, sticky TOP masthead,
# second sans family with no serif fallback — every fake must fail its check.
rc, out = _run([str(VO), str(EX / "redteam-premium-gamed.html"),
                "--lock", str(EX / "premium-lock.json"), "--tier", "premium", "--json"])
gm = json.loads(out)
check(
    "red team: gamed elevate heuristics (hidden hero, sticky masthead, two-sans) all FAIL",
    rc == 1 and gm["elevatePass"] is False
    and {c["check"] for c in gm["elevateChecks"] if c["status"] == "fail"}
    == {"full-bleed hero section", "legibility scrim over hero imagery",
        "display type system (serif display + sans body)", "sticky action bar"},
)

# Failure class 2: a deliverable that ignores the brief's structure and disguises it.
rc, out = _run([str(VC), str(EX / "redteam-conformance-evasion.html"),
                "--structure", str(EX / "structure-fixture.json"), "--json"])
ce = json.loads(out)
check(
    "red team: reformatted banned header (case/quotes/multi-class) still caught",
    rc == 1 and 'class="custom-header"' in ce["forbiddenHits"],
)
check("red team: empty stub faking a required section caught", any("proof" in s for s in ce["stubSections"]))
check("red team: reordered required sections caught", bool(ce["orderViolations"]))
check(
    "red team: placeholder hidden while a guessed value ships caught",
    "[CLIENT_PHONE]" in ce["hiddenPlaceholders"],
)

# Failure class 3: the original off-palette generic clone must still fail the brand audit —
# asserted here explicitly for the v1.1 acceptance map (full coverage lives in the v1.0 cases above).
rc, out = vo_run("redteam-original-failure.html", "lock-fixture.json")
check("red team: original off-palette generic clone still FAILS the brand audit", rc == 1)

# Run-level forgeries against the new gates.
d = copy.deepcopy(prem_base)
d["outputAudit"]["elevatePass"] = True
d["outputAudit"]["elevateChecks"] = []
rc, out = vr_obj(d)
check(
    "red team: bare elevatePass with no elevateChecks REJECTED as hand-asserted",
    rc == 1 and "elevatechecks" in out.lower(),
)

d = copy.deepcopy(prem_base)
d["outputAudit"]["elevateChecks"] = copy.deepcopy(d["outputAudit"]["elevateChecks"])
d["outputAudit"]["elevateChecks"][0]["status"] = "fail"
rc, out = vr_obj(d)
check(
    "red team: elevatePass true over a failing elevate check REJECTED as inconsistent",
    rc == 1 and "inconsistent" in out.lower(),
)

d = copy.deepcopy(prem_base)
d["conformance"] = {**d["conformance"], "pass": True, "missingSections": ["proof"]}
rc, out = vr_obj(d)
check(
    "red team: conformance pass flipped true over listed violations REJECTED",
    rc == 1 and "inconsistent" in out.lower(),
)

d = copy.deepcopy(prem_base)
d["brief"]["tier"] = "Custom"
d["trace"][1]["modelTier"] = "standard"
d["tierSignoff"] = {"by": "N/A"}
rc, out = vr_obj(d)
check(
    "red team: Custom tierSignoff.by = 'N/A' placeholder REJECTED",
    rc == 1 and "tiersignoff" in out.lower(),
)

# Regression guard for the var() fix: custom properties NAMED after colors are not misread as
# named colors (in-lock deliverable using --navy/--coral variables must pass), while a real color
# hidden in a var() FALLBACK is still caught.
with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
    f.write(
        "<style>:root{--navy:#062456;--coral:#FF5747}"
        "body{background:var(--navy);color:#FFFFFF;font-family:Quicksand,Arial,sans-serif}"
        ".c{background:var(--coral)}</style><h1>Reserve Your Boat</h1>"
    ); var_ok_path = f.name
rc, out = _run([str(VO), var_ok_path, "--lock", str(EX / "lock-fixture.json"), "--json"])
check("regression: color-word var() names no longer false-positive as named colors", rc == 0 and json.loads(out)["pass"] is True)
with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
    f.write(
        "<style>body{background:#062456;color:var(--x, rebeccapurple);font-family:Quicksand}</style><p>hi</p>"
    ); var_bad_path = f.name
rc, out = _run([str(VO), var_bad_path, "--lock", str(EX / "lock-fixture.json"), "--json"])
check("red team: off-lock named color in a var() fallback still caught", rc == 1 and "#663399" in json.loads(out)["colorsOutOfLock"])

# ---- v1.1.0 dogfood: the Premium pipeline run on revüe's own launch page stays reproducible ----
DOGP = EX / "dogfood-premium"
rc, out = _run([str(VO), str(DOGP / "winner-draft-1.html"), "--lock", str(DOGP / "lock.json"),
                "--tier", "premium", "--json"])
dp1 = json.loads(out)
check(
    "dogfood-premium: clean-template draft fails ALL FOUR elevate checks while base audit is clean",
    rc == 1 and dp1["elevatePass"] is False and not dp1["colorsOutOfLock"] and not dp1["fontsOutOfLock"]
    and sum(1 for c in dp1["elevateChecks"] if c["status"] == "fail") == 4,
)
rc, _ = _run([str(VC), str(DOGP / "winner-draft-1.html"), "--structure", str(DOGP / "structure.json")])
check("dogfood-premium: the same draft CONFORMS structurally — only the tier gate catches it", rc == 0)
rc, _ = _run([str(VO), str(DOGP / "winner.html"), "--lock", str(DOGP / "lock.json"), "--tier", "premium"])
check("dogfood-premium: rebuilt winner passes the full Premium audit", rc == 0)
rc, _ = _run([str(VC), str(DOGP / "winner.html"), "--structure", str(DOGP / "structure.json")])
check("dogfood-premium: rebuilt winner passes conformance ([LAUNCH_DATE] visibly intact)", rc == 0)
dogp_run = json.loads((DOGP / "run.json").read_text(encoding="utf-8"))
rc, _ = _run([str(VR), str(DOGP / "run.json"), "--strict"])
check("dogfood-premium: full run artifact validates (strict)", rc == 0)

# Both directions from the same artifact: a genuinely Premium output MAY ship...
d = copy.deepcopy(dogp_run); d["verdict"]["value"] = "ship"
rc, _ = vr_obj(d)
check("dogfood-premium: flipped to 'ship' with the real passing audits, validates", rc == 0)
# ...and the same ship claim over the clean-template draft's audit is rejected as Standard-bar-only.
d = copy.deepcopy(dogp_run); d["verdict"]["value"] = "ship"
d["outputAudit"] = {**dp1, "deliverablePath": "examples/dogfood-premium/winner-draft-1.html"}
rc, out = vr_obj(d)
check(
    "dogfood-premium: 'ship' over the clean-template draft audit REJECTED as Standard-bar-only",
    rc == 1 and "standard bar" in out.lower(),
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
