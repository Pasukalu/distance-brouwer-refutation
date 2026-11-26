"""Fail the build if the Lean sources stop being axiom-hygienic.

Checks, for every *.lean file in lean/:
  * no `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `partial`
    outside comments;
  * the number of `#print axioms` audit lines is exactly 18;
  * prints the audited theorem names so reviewers can diff them against
    verification/formalization-coverage.md.

Exit code 1 on violation. Pure standard library.
"""
import re
import sys
from pathlib import Path

LEAN_DIR = Path(__file__).resolve().parent.parent / "lean"
FORBIDDEN = {
    "sorry": r"(?<![\w'])sorry(?![\w'])",
    "admit": r"(?<![\w'])admit(?![\w'])",
    "axiom": r"^\s*axiom\s",
    "native_decide": r"\bnative_decide\b",
    "unsafe": r"^\s*unsafe\s",
    "partial": r"^\s*partial\s",
}
EXPECTED_AXIOM_AUDITS = 18


def strip_comments(text: str) -> str:
    """Remove -- line comments and /- -/ block comments (non-nested is enough here)."""
    text = re.sub(r"/-.*?-/", "", text, flags=re.S)
    return re.sub(r"--[^\n]*", "", text)


def main() -> int:
    files = sorted(LEAN_DIR.glob("*.lean"))
    if not files:
        print(f"no .lean files under {LEAN_DIR}")
        return 1
    problems = []
    audits = []
    for path in files:
        raw = path.read_text(encoding="utf-8")
        code = strip_comments(raw)
        for name, pattern in FORBIDDEN.items():
            for m in re.finditer(pattern, code, flags=re.M):
                line = code[: m.start()].count("\n") + 1
                problems.append(f"{path.name}:{line}: forbidden `{name}`")
        audits += [ln.strip() for ln in code.splitlines() if ln.strip().startswith("#print axioms")]
    if len(audits) != EXPECTED_AXIOM_AUDITS:
        problems.append(
            f"expected {EXPECTED_AXIOM_AUDITS} `#print axioms` audit lines, found {len(audits)}"
        )
    print(f"scanned {len(files)} Lean files; {len(audits)} axiom audits")
    for a in audits:
        print("  audit:", a.replace("#print axioms ", "").strip())
    if problems:
        print("\nHYGIENE CHECK FAILED:")
        for p in problems:
            print("  -", p)
        return 1
    print("\nHYGIENE CHECK PASSED: no sorry/admit/axiom/native_decide/unsafe/partial")
    return 0


if __name__ == "__main__":
    sys.exit(main())
