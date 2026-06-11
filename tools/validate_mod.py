#!/usr/bin/env python3
"""Lint the HOI4 mods in this repo.

Checks (per mod folder under mods/):
  1. Paradox-script files parse: balanced braces outside comments/strings.
  2. Focus ids unique; prerequisite / relative_position_id /
     mutually_exclusive reference existing focus ids.
  3. No two focuses resolve to the same absolute (x, y).
  4. Every focus has loc NAME and NAME_desc; every idea has NAME + NAME_desc.
  5. Every `country_event = { id = ... }` / `country_event = ns.N` fired
     anywhere exists in the events files.
  6. localisation/**.yml files start with the UTF-8 BOM.

Usage:  python3 tools/validate_mod.py [mod_name] [--mods-dir PATH]
Exit 0 = clean, 1 = findings (printed).
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MODS = REPO / "mods"

def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        in_str = False
        for i, ch in enumerate(line):
            if ch == '"':
                in_str = not in_str
            elif ch == '#' and not in_str:
                line = line[:i]
                break
        out.append(line)
    return "\n".join(out)

def brace_check(path: Path, findings: list):
    txt = strip_comments(path.read_text(encoding="utf-8-sig"))
    depth = 0
    for n, line in enumerate(txt.splitlines(), 1):
        for ch in line:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth < 0:
                    findings.append(f"{path}:{n}: unbalanced '}}'")
                    return
    if depth != 0:
        findings.append(f"{path}: {depth} unclosed '{{'")

def parse_focus_blocks(text: str):
    """Yield dicts for each `focus = { ... }` block (shallow key scan)."""
    txt = strip_comments(text)
    focuses = []
    i = 0
    while True:
        m = re.search(r"\bfocus\s*=\s*\{", txt[i:])
        if not m:
            break
        start = i + m.end()
        depth = 1
        j = start
        while depth and j < len(txt):
            if txt[j] == '{':
                depth += 1
            elif txt[j] == '}':
                depth -= 1
            j += 1
        body = txt[start:j - 1]
        focuses.append(body)
        i = j
    return focuses

def scalar(body: str, key: str):
    m = re.search(rf"\b{key}\s*=\s*([\w\.\-]+)", body)
    return m.group(1) if m else None

def all_refs(body: str, key: str):
    """All `focus = X` ids inside key = { ... } sub-blocks."""
    refs = []
    for m in re.finditer(rf"\b{key}\s*=\s*\{{([^{{}}]*)\}}", body):
        refs += re.findall(r"\bfocus\s*=\s*(\w+)", m.group(1))
    return refs

def check_focus_tree(mod: Path, loc_keys: set, event_ids: set, findings: list):
    nf = mod / "common" / "national_focus"
    if not nf.is_dir():
        return
    focuses = {}
    for f in nf.glob("*.txt"):
        for body in parse_focus_blocks(f.read_text(encoding="utf-8-sig")):
            fid = scalar(body, "id")
            if fid in focuses:
                findings.append(f"{f}: duplicate focus id {fid}")
            focuses[fid] = body
    # references + loc + fired events
    for fid, body in focuses.items():
        for ref in all_refs(body, "prerequisite") + all_refs(body, "mutually_exclusive"):
            if ref not in focuses:
                findings.append(f"focus {fid}: dangling reference {ref}")
        rel = scalar(body, "relative_position_id")
        if rel and rel not in focuses:
            findings.append(f"focus {fid}: dangling relative_position_id {rel}")
        if fid not in loc_keys:
            findings.append(f"focus {fid}: missing loc key")
        if f"{fid}_desc" not in loc_keys:
            findings.append(f"focus {fid}: missing loc key {fid}_desc")
        for ev in re.findall(r"country_event\s*=\s*(?:\{\s*id\s*=\s*)?([\w\.]+)", body):
            if ev not in event_ids:
                findings.append(f"focus {fid}: fires unknown event {ev}")
    # absolute positions
    def abs_pos(fid, seen=None):
        seen = seen or set()
        if fid in seen:
            return None  # cycle; reported separately
        seen.add(fid)
        body = focuses[fid]
        x = int(scalar(body, "x") or 0)
        y = int(scalar(body, "y") or 0)
        rel = scalar(body, "relative_position_id")
        if rel and rel in focuses:
            p = abs_pos(rel, seen)
            if p is None:
                return None
            return (x + p[0], y + p[1])
        return (x, y)
    cells = {}
    for fid in focuses:
        p = abs_pos(fid)
        if p is None:
            findings.append(f"focus {fid}: relative_position cycle")
        elif p in cells:
            findings.append(f"focus {fid}: position {p} collides with {cells[p]}")
        else:
            cells[p] = fid

# Structural keys that are not idea names — these appear as depth-2 blocks
# inside slot blocks (e.g. country = { <slot_key> = { modifier = { ... } } })
# but are properties of an idea, not idea names themselves.
IDEA_STRUCTURAL_KEYS = {
    "modifier", "targeted_modifier", "equipment_bonus", "research_bonus",
    "allowed", "allowed_civil_war", "available", "visible", "ai_will_do",
    "picture", "removal_cost", "on_add", "on_remove", "rule", "cancel",
}

def check_ideas(mod: Path, loc_keys: set, findings: list):
    ideas_dir = mod / "common" / "ideas"
    if not ideas_dir.is_dir():
        return
    for f in ideas_dir.glob("*.txt"):
        txt = strip_comments(f.read_text(encoding="utf-8-sig"))
        # idea names: keys at depth 2 inside ideas = { <slot> = { NAME = { ... } } }
        for m in re.finditer(r"^\t\t(\w+)\s*=\s*\{", txt, re.M):
            name = m.group(1)
            if name in IDEA_STRUCTURAL_KEYS:
                continue
            if name not in loc_keys:
                findings.append(f"idea {name}: missing loc key")
            if f"{name}_desc" not in loc_keys:
                findings.append(f"idea {name}: missing loc key {name}_desc")

def collect_loc(mod: Path, findings: list) -> set:
    keys = set()
    loc = mod / "localisation"
    if not loc.is_dir():
        return keys
    for f in loc.rglob("*.yml"):
        raw = f.read_bytes()
        if not raw.startswith(b"\xef\xbb\xbf"):
            findings.append(f"{f}: missing UTF-8 BOM (descriptions will render blank)")
        for m in re.finditer(r"^\s([\w\.]+):\d?\s", raw.decode("utf-8-sig"), re.M):
            keys.add(m.group(1))
    return keys

def collect_events(mod: Path) -> set:
    ids = set()
    ev = mod / "events"
    if not ev.is_dir():
        return ids
    for f in ev.glob("*.txt"):
        txt = strip_comments(f.read_text(encoding="utf-8-sig"))
        ids |= set(re.findall(r"\bid\s*=\s*([\w]+\.\d+)", txt))
    return ids

def main():
    parser = argparse.ArgumentParser(description="Lint HOI4 mods in this repo.")
    parser.add_argument("mod_name", nargs="?", help="Only lint this mod (by folder name).")
    parser.add_argument("--mods-dir", type=Path, default=MODS,
                        help="Path to the mods directory (default: <repo>/mods).")
    args = parser.parse_args()

    mods_dir = args.mods_dir
    target = args.mod_name
    findings = []
    for mod in sorted(mods_dir.iterdir()):
        if not mod.is_dir() or (target and mod.name != target):
            continue
        for f in mod.rglob("*.txt"):
            brace_check(f, findings)
        loc_keys = collect_loc(mod, findings)
        event_ids = collect_events(mod)
        check_focus_tree(mod, loc_keys, event_ids, findings)
        check_ideas(mod, loc_keys, findings)
    for line in findings:
        print(f"FAIL {line}")
    print(f"{'CLEAN' if not findings else f'{len(findings)} finding(s)'}")
    return 1 if findings else 0

if __name__ == "__main__":
    sys.exit(main())
