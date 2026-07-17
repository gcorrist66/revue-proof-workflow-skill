#!/usr/bin/env python3
"""Generate the self-contained revüe installer (apply-revue-<version>.sh).

Embeds every distributable file in the repo as base64 into a single shell script. Running that script
recreates the full skill tree in a target directory and then runs the complete eval suite inside it —
the installer exits non-zero and reports failure unless every eval passes. An install that cannot
prove its own guarantees is not an install.

Usage:
    python3 scripts/make-installer.py [--version 1.0.0] [--out dist/]

Stdlib only. Paths are stored relative to the repo root — no machine paths are embedded.
"""

from __future__ import annotations

import argparse
import base64
import os
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {".git", "__pycache__", "dist", "build", ".venv", "venv", ".DS_Store"}
EXCLUDE_FILES = {"scratch.tmp", ".DS_Store"}
EXCLUDE_SUFFIXES = {".pyc", ".zip"}


def distributable_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if rel.name in EXCLUDE_FILES or rel.suffix in EXCLUDE_SUFFIXES:
            continue
        files.append(rel)
    return files


FOOTER = """
echo "revüe {version}: files written. Running the eval suite (the install gates on it)..."
if ! python3 "$TARGET/scripts/run-evals.py"; then
  echo ""
  echo "revüe {version}: INSTALL FAILED — the eval suite did not pass in the applied tree." >&2
  echo "The guarantees are not proven; do not use this install." >&2
  exit 1
fi
echo ""
echo "revüe {version}: installed and proven — all evals green in $TARGET"
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the self-contained revüe installer.")
    parser.add_argument("--version", default="1.0.0")
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    args = parser.parse_args()

    files = distributable_files()
    name = f"apply-revue-v{args.version}.sh"
    out_path = args.out / name
    args.out.mkdir(parents=True, exist_ok=True)

    chunks: list[str] = [
        "#!/usr/bin/env bash\n"
        f"# revüe {args.version} — self-contained installer.\n"
        "# Recreates the full skill tree in TARGET_DIR (default: ./revue-proof-workflow), then runs\n"
        "# the complete eval suite inside it. The install FAILS unless every eval passes — the suite\n"
        "# is the trust anchor, and this installer gates on it.\n"
        "#\n"
        f"# Usage:  bash {name} [TARGET_DIR]\n"
        "set -euo pipefail\n\n"
        'TARGET="${1:-./revue-proof-workflow}"\n'
        'mkdir -p "$TARGET"\n'
        f'echo "revüe {args.version}: writing {len(files)} files into $TARGET"\n\n'
        "write_file() {\n"
        '  local path="$TARGET/$1"\n'
        '  mkdir -p "$(dirname "$path")"\n'
        '  base64 -d > "$path"\n'
        "}\n\n"
    ]

    for rel in files:
        data = (ROOT / rel).read_bytes()
        b64 = base64.encodebytes(data).decode("ascii")
        chunks.append(f"write_file '{rel.as_posix()}' <<'__REVUE_B64__'\n{b64}__REVUE_B64__\n")
        if (ROOT / rel).stat().st_mode & stat.S_IXUSR:
            chunks.append(f"chmod +x \"$TARGET/{rel.as_posix()}\"\n")
        chunks.append("\n")

    chunks.append(FOOTER.format(version=args.version))
    out_path.write_text("".join(chunks), encoding="utf-8")
    out_path.chmod(out_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    size_kb = out_path.stat().st_size // 1024
    print(f"wrote {out_path.relative_to(ROOT) if out_path.is_relative_to(ROOT) else out_path} "
          f"({len(files)} files embedded, {size_kb} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
