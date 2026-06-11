# USA Focus Tree Overhaul ("Wings of the Eagle") Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the 53-focus Presidential Cabinet tree with a ~170-focus 1936–1956 tree (trunk + four ideology wings + shared military pillar), every focus carrying a written description, validated by a repo linter.

**Architecture:** One focus-tree file organized as TRUNK / DEM / GOP / RADICAL / AUTH / MILITARY sections positioned off per-wing anchor focuses; a generalized cabinet system (scripted effects + power balance + per-era idea slates); election event chains as chapter breaks. A Python linter (`tools/validate_mod.py`) is the test harness: every task ends with a clean validator run.

**Tech Stack:** HOI4 Paradox script (focus trees, ideas, events, scripted effects, power balance), HOI4 localisation YML (UTF-8 **with BOM**), Python 3 (validator, stdlib only).

**Spec:** `docs/superpowers/specs/2026-06-10-usa-focus-tree-overhaul-design.md`

---

## File structure

| File | Responsibility |
|---|---|
| `tools/validate_mod.py` | **Create.** Repo-level linter: braces, unique ids, dangling refs, position collisions, loc coverage incl. `_desc`, event-id existence, BOM check |
| `mods/usa_presidential_cabinet/common/national_focus/usa_cabinet.txt` | **Rewrite.** The full tree, six commented sections, wing anchors |
| `mods/usa_presidential_cabinet/common/scripted_effects/usa_cabinet_effects.txt` | **Extend.** Cabinet clear/reset, era flags, election resolver helpers |
| `mods/usa_presidential_cabinet/common/ideas/usa_cabinet_ideas.txt` | **Extend.** ~40 cabinet spirits (all eras/slates) + wing spirits |
| `mods/usa_presidential_cabinet/common/power_balance/usa_cabinet_power_balance.txt` | **Keep**; side loc swapped via scripted localisation |
| `common/scripted_localisation/usa_cabinet_scripted_loc.txt` | **Create.** Balance side names per wing flag |
| `mods/usa_presidential_cabinet/events/usa_cabinet_events.txt` | **Extend.** Five election chains, coup/succession, era transitions (~35 events, namespace `usa_cabinet`) |
| `mods/usa_presidential_cabinet/common/on_actions/usa_cabinet_on_actions.txt` | **Extend.** Startup + war/peace flag wiring |
| `mods/usa_presidential_cabinet/localisation/english/usa_cabinet_l_english.yml` | **Rewrite.** Name + desc for every focus/idea/event |
| `mods/usa_presidential_cabinet/README.md` + `descriptor.mod` | **Update.** Features, version 0.3.0 |

### Position scheme (absolute x, y in tree cells)

- Trunk: x 19–21. Radical wing x 1–7, Dem wing x 9–17, GOP x 23–31, Auth x 33–39, Military x 42–46.
- Era bands (y): 1936–39 → 0–5 · 1940–43 → 6–11 · 1944–47 → 12–17 · 1948–51 → 18–23 · 1952–56 → 24–29.
- Each wing's first focus is its **anchor**; every other wing focus uses `relative_position_id` of that anchor (or a later same-wing focus).

### Naming conventions

- Focus ids: `USA_<wing>_<slug>` with wing ∈ `trunk, dem, gop, rad, auth, mil` (e.g. `USA_dem_lend_lease`). Existing cabinet appointment ids (`USA_appoint_hull`, …) keep their names for save-compat with the '36 slate; new-era appointments use `USA_cab<era>_<name>` (e.g. `USA_cab48_marshall`).
- Era flags: `USA_era_1940`, `USA_era_1944`, `USA_era_1948`, `USA_era_1952` (set by election resolution events).
- Wing flags: `USA_wing_dem`, `USA_wing_gop`, `USA_wing_rad`, `USA_wing_auth` (set by commitment focuses).
- Events: `usa_cabinet.100–199` elections, `.200–249` coups/succession, `.250–299` era flavor.

---

### Task 1: The validator (`tools/validate_mod.py`)

**Files:**
- Create: `tools/validate_mod.py`
- Test: running it against the *current* mod is the test

- [ ] **Step 1: Write the validator**

```python
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

Usage:  python3 tools/validate_mod.py [mod_name]
Exit 0 = clean, 1 = findings (printed).
"""
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

BLOCK_RE = re.compile(r"(\w+)\s*=\s*\{")

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

def check_ideas(mod: Path, loc_keys: set, findings: list):
    for f in (mod / "common" / "ideas").glob("*.txt") if (mod / "common" / "ideas").is_dir() else []:
        txt = strip_comments(f.read_text(encoding="utf-8-sig"))
        # idea names: keys at depth 2 inside ideas = { <slot> = { NAME = { ... } } }
        for m in re.finditer(r"^\t\t(\w+)\s*=\s*\{", txt, re.M):
            name = m.group(1)
            if name in ("modifier", "targeted_modifier", "equipment_bonus", "research_bonus", "allowed", "allowed_civil_war", "available", "visible", "ai_will_do", "picture", "removal_cost", "on_add", "on_remove", "rule", "cancel"):
                continue
            if name not in loc_keys:
                findings.append(f"idea {name}: missing loc key")
            if f"{name}_desc" not in loc_keys:
                findings.append(f"idea {name}: missing loc key {name}_desc")

def collect_loc(mod: Path, findings: list) -> set:
    keys = set()
    loc = mod / "localisation"
    for f in loc.rglob("*.yml") if loc.is_dir() else []:
        raw = f.read_bytes()
        if not raw.startswith(b"\xef\xbb\xbf"):
            findings.append(f"{f}: missing UTF-8 BOM (descriptions will render blank)")
        for m in re.finditer(r"^\s([\w\.]+):\d?\s", raw.decode("utf-8-sig"), re.M):
            keys.add(m.group(1))
    return keys

def collect_events(mod: Path) -> set:
    ids = set()
    ev = mod / "events"
    for f in ev.glob("*.txt") if ev.is_dir() else []:
        txt = strip_comments(f.read_text(encoding="utf-8-sig"))
        ids |= set(re.findall(r"\bid\s*=\s*([\w]+\.\d+)", txt))
    return ids

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    findings = []
    for mod in sorted(MODS.iterdir()):
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
```

- [ ] **Step 2: Run against the current mod — expect it to surface real gaps (the old tree is missing many `_desc` keys); fix validator bugs, not mod content, at this stage**

Run: `python3 tools/validate_mod.py usa_presidential_cabinet`
Expected: a finding list (missing `_desc` keys at minimum), no Python tracebacks.

- [ ] **Step 3: Sanity-check the checks** — deliberately break a copy (remove one `}`; rename one focus's prerequisite to `USA_nope`) in `/tmp`, point the script at it, confirm both are caught, restore.

- [ ] **Step 4: Commit**

```bash
git add tools/validate_mod.py
git commit -m "tools: add validate_mod.py linter (braces, refs, positions, loc, BOM)"
```

---

### Task 2: Tree skeleton — root, anchors, era scaffolding

**Files:**
- Rewrite: `mods/usa_presidential_cabinet/common/national_focus/usa_cabinet.txt` (keep `focus_tree` header/id/country block, replace all focuses)
- Modify: `localisation/english/usa_cabinet_l_english.yml` (fresh header + keys for the skeleton focuses)
- Modify: `common/scripted_effects/usa_cabinet_effects.txt` (era/wing flag helpers)

- [ ] **Step 1: Write the trunk root + five era anchors + five wing anchors** (these are real playable focuses, not dummies). Skeleton (positions absolute on root, all other sections will hang off these):

```
focus = {
	id = USA_trunk_inheritance_of_32          # root, x=20 y=0, cost 5
	# effect: 120 political_power is NOT given here; gives USA_depression_era idea removal kickoff
}
focus = { id = USA_dem_anchor    x=13 y=1  prerequisite USA_trunk_inheritance_of_32 }   # "The New Deal Coalition"
focus = { id = USA_gop_anchor    x=27 y=1  prerequisite USA_trunk_inheritance_of_32 }   # "The Loyal Opposition"
focus = { id = USA_rad_anchor    x=4  y=1  prerequisite USA_trunk_inheritance_of_32 }   # "Voices of Discontent"
focus = { id = USA_auth_anchor   x=36 y=1  prerequisite USA_trunk_inheritance_of_32 }   # "The Whispering Gallery"
focus = { id = USA_mil_anchor    x=44 y=0 }                                             # "The Arsenal Question" (no prereq: military always open)
```

Scripted effects to add now (used by everything later):

```
USA_set_era_flag_1940 = { set_country_flag = USA_era_1940 }
USA_set_era_flag_1944 = { set_country_flag = USA_era_1944 }
USA_set_era_flag_1948 = { set_country_flag = USA_era_1948 }
USA_set_era_flag_1952 = { set_country_flag = USA_era_1952 }
USA_clear_cabinet = {
	# remove every cabinet seat idea from any era (add each new idea id here as slates are added)
	remove_ideas = { USA_cab_hull USA_cab_isolationist_state USA_cab_morgenthau USA_cab_business_treasury USA_cab_stimson USA_cab_woodring USA_cab_murphy USA_cab_security_ag }
	set_variable = { USA_cabinet_seats_filled = 0 }
}
```

- [ ] **Step 2: Loc for the six anchors (name + `_desc`, period voice)** — write final prose now; e.g. `USA_trunk_inheritance_of_32_desc:0 "Four years after the Crash the banks have reopened, but a quarter of the nation still stands idle. Whatever Washington becomes in the next twenty years begins with what it does about the Depression."`

- [ ] **Step 3: Validate** — `python3 tools/validate_mod.py usa_presidential_cabinet` → CLEAN (old focuses are gone, skeleton fully loc'd).

- [ ] **Step 4: Commit** — `git commit -m "tree: skeleton — trunk root, wing anchors, era effects"`

---

### Task 3: The Election of 1936 — the full election pattern (focus + events + cabinet '36)

This task establishes the *complete* pattern every later election copies.

**Files:**
- Modify: `common/national_focus/usa_cabinet.txt` (trunk '36 cluster + cabinet '36 appointment focuses, ported from the old tree)
- Modify: `events/usa_cabinet_events.txt` (events `usa_cabinet.100–104`)
- Modify: `common/ideas/usa_cabinet_ideas.txt` (port the 8 existing '36 cabinet ideas, renamed to `USA_cab_*`)
- Modify: loc

- [ ] **Step 1: Port the '36 cabinet** (Brain Trust focus + 4 seats × 2 candidates) from the old tree under the trunk, positions y=2–4 relative to root, ids kept (`USA_appoint_hull` …), ideas renamed with a `USA_cab_` prefix and listed in `USA_clear_cabinet`.

- [ ] **Step 2: Election focus + chain.** Focus `USA_trunk_election_1936` (x=20, rel root, y=5; available `date > 1936.6.1`; bypass if at war). On complete → `country_event = usa_cabinet.100`.

```
usa_cabinet.100  "The Election of 1936"        options: campaign on the New Deal (→.101) / let the cabinet's balance decide (→ resolver) / [wing_rad invested] back a third-party surge (→.102)
usa_cabinet.101  "Roosevelt Triumphant"        FDR re-elected: stability +5%, era flag 1940 via USA_set_era_flag_1940, USA_clear_cabinet does NOT fire ('36→'40 continuity is the one exception)
usa_cabinet.102  "A House Divided"             hung outcome: PP −50, sets USA_election_upset flag (rad/auth wings read it)
usa_cabinet.103  "Landon!"                     GOP upset (fires only if GOP wing invested ≥3 focuses): leader swap to Landon, USA_clear_cabinet, era flag, GOP '40 slate unlocks early
usa_cabinet.104  era transition flavor "A New Term Begins"
```

- [ ] **Step 3: Loc** — full prose for the five events + election focus (+ options).

- [ ] **Step 4: Validate + commit** — `git commit -m "trunk: 1936 — Brain Trust cabinet + Election of 1936 chain"`

---

### Task 4: Trunk completion — elections '40–'52, war pivots, on-ramps

**Files:** national_focus, events (`usa_cabinet.110–149, 200–219`), scripted_effects (election resolver), on_actions (war/peace flags), loc

- [ ] **Step 1: Election focuses.** `USA_trunk_election_1940/1944/1948/1952` at y=11/17/23/29 on trunk x=20. Availability: date window + prior election anchor completed. Each fires its chain (`.110+`, `.120+`, `.130+`, `.140+`) following the Task-3 pattern; **each completion runs `USA_clear_cabinet` + the era flag + unlocks the era's slates** (the '36 continuity exception aside).
- [ ] **Step 2: Resolver effect.** `USA_resolve_election = { ... }` reads power-balance side + wing flags and sets `USA_election_winner_<wing>` flag; chains' "let the country decide" options call it.
- [ ] **Step 3: War pivots.** `USA_trunk_infamy` (avail: at war with a major OR `USA_wing_auth`; bypass via war), `USA_trunk_shape_of_the_peace` (avail: enemy capitulated or peace flag). On_action `on_war` / `on_peace` set `USA_at_war` / `USA_postwar` flags used by era gates.
- [ ] **Step 4: Authoritarian on-ramps.** `USA_trunk_third_term_crisis` (y=10, mut-excl with election_1940's democratic resolution — selecting it locks `USA_wing_auth` available) and `USA_trunk_suspended_election` (y=16, requires at-war + auth wing) → events `usa_cabinet.200/.201` (constitutional crisis flavor, PP and stability shocks, Caesar path opens).
- [ ] **Step 5: Loc for everything (~20 focuses/events), validate, commit** — `git commit -m "trunk: elections 1940-52, war pivots, authoritarian on-ramps"`

---

### Task 5: Democratic wing, 1936–1944 (≈18 focuses)

**Files:** national_focus (DEM section), ideas (2 wing spirits), events (`.250–.254` flavor), loc

Roster (all `relative_position_id` chained from `USA_dem_anchor`; cost 10 unless noted; ✋ = cabinet-gated):

| id | band | prereq | gate/excl | effect sketch | desc brief |
|---|---|---|---|---|---|
| `USA_dem_second_new_deal` | '36 | anchor | — | +2 civ factories East | WPA/Wagner act second wave |
| `USA_dem_wagner_act` | '36 | ^ | — | stability +5, +Labor spirit | labor peace through recognition |
| `USA_dem_social_security` | '36 | ^ | — | consumer goods −2% | the old-age compact |
| `USA_dem_court_fight` | '37 | second_new_deal | excl `USA_gop_nine_old_men_win` | PP −75 then +120 | court-packing gamble |
| `USA_dem_commitment` | '37 | any 2 dem | **commitment**: excl gop/rad/auth commitments; sets `USA_wing_dem` | +5% stability | the coalition holds |
| `USA_dem_rearmament_politics` | '38 | commitment | ✋ War=Stimson | army XP +25, mil factory | selling preparedness to a peace-minded public |
| `USA_dem_cash_and_carry` | '39 | ^ | ✋ State=Hull | trade-law unlocks, UK opinion | neutrality bends toward the democracies |
| `USA_dem_destroyers_for_bases` | '40 | ^ | — | give UK 50 convoys → bases spirit | the fifty old ships |
| `USA_dem_lend_lease` | '41 | ^ | ✋ State=Hull | lend-lease capacity spirit | arsenal opens its books |
| `USA_dem_arsenal_of_democracy` | '41 | lend_lease | — | +3 mil factories | conversion of an economy |
| `USA_dem_wpb` | '42 | arsenal | requires `USA_at_war` | −20% mil construction cost | the War Production Board |
| `USA_dem_osrd` | '42 | arsenal | — | +1 research slot | science mobilized |
| `USA_dem_atlantic_charter` | '41 | lend_lease | — | Allies opinion, war-aims spirit | a meeting at Placentia Bay |
| `USA_dem_tehran` | '43 | atlantic_charter + at_war | — | SOV opinion, planning bonus | the Big Three convene |
| `USA_dem_yalta` | '45 band edge | tehran | — | postwar flags | dividing the world to save it |
| `USA_dem_double_v` | '42 | wpb | — | manpower +2%, stability +2% | home-front integration steps |
| `USA_dem_gi_bill_groundwork` | '44 | wpb | — | postwar growth flag | repaying the uniform |
| `USA_dem_president_is_dead` | '45 | yalta, date>1945.1 | — | event `.205` Truman succession (leader swap, cabinet partial reset) | the haberdasher takes the oath |

- [ ] **Step 1: Write the 18 focuses** (positions: band rows under anchor, two columns x±1 to keep the wing ≤3 wide).
- [ ] **Step 2: Succession event `.205`** (Truman portrait swap, Wallace alt-option if rad influence high).
- [ ] **Step 3: Loc — names + final 1–3 sentence descriptions for all 18 + events.** The desc briefs above are the content spec; write them in period voice.
- [ ] **Step 4: Validate, commit** — `git commit -m "dem wing: 1936-44 — New Deal to Yalta"`

---

### Task 6: Democratic wing, 1945–1956 (≈17 focuses)

Same files. Roster:

| id | band | prereq | gate | effect sketch | desc brief |
|---|---|---|---|---|---|
| `USA_dem_bretton_woods` | '45 | era_1944 + postwar-or-1946 | — | +10% trade, gold-window spirit | dollar becomes the anchor |
| `USA_dem_united_nations` | '45 | shape_of_the_peace | — | PP +120, UN spirit | Dumbarton Oaks made real |
| `USA_dem_containment` | '47 | un | ✋ State internationalist | enables guarantees | the long telegram heeded |
| `USA_dem_truman_doctrine` | '47 | containment | — | Greece/Turkey guarantees | aid to free peoples |
| `USA_dem_marshall_plan` | '48 | truman_doctrine | — | send 3 civ-factory equivalents, Euro opinion ladder | rebuilding the customers |
| `USA_dem_nato` | '49 | marshall_plan | — | faction unlock "North Atlantic Treaty" | an entangling alliance at last |
| `USA_dem_fair_deal` | '49 | era_1948 | — | stability +5, consumer −2% | New Deal's second act |
| `USA_dem_nsc68` | '50 | containment | — | +0.5% recruitable, +2 mil | rearming the peace |
| `USA_dem_korea_line` | '50 | nsc68 | at_war_or_flag | war-goal/volunteers toward Korea-flag | drawing the line at the 38th |
| `USA_dem_red_scare_managed` | '50 | era_1948 | ✋ AG civil-libertarian | stability +3 vs PP −50 choice event | loyalty boards with limits |
| `USA_dem_election_52_ike` | '52 | era_1952 | excl `_egghead` | leader Eisenhower (GOP-internationalist coloring) | the general comes home |
| `USA_dem_election_52_egghead` | '52 | era_1952 | excl `_ike` | leader Stevenson | eloquence against the tide |
| `USA_dem_new_look` | '53 | either '52 | — | air XP, nuke production +25% | more bang for the buck |
| `USA_dem_atoms_for_peace` | '54 | new_look | — | research bonus nuclear, world tension −5 | the peaceful atom |
| `USA_dem_interstate` | '56 | either '52 | — | +4 infrastructure spread | ribbons of concrete |
| `USA_dem_saint_lawrence` | '55 | either '52 | — | +1 civ, +dockyard | the seaway compact |
| `USA_dem_hundred_million_strong` | '56 | interstate | — | victory-lap spirit (growth) | the affluent society |

- [ ] **Step 1–4: focuses → loc (final prose) → validate → commit** `git commit -m "dem wing: 1945-56 — Bretton Woods to the Affluent Society"`

---

### Task 7: Republican wing (≈30 focuses, two sub-tasks '36–'44 / '45–'56)

Same file pattern. Key roster (compressed; same column discipline):

'36–'44: `USA_gop_landon_banner` (anchor child) → `USA_gop_nine_old_men_win` (excl dem court_fight) → `USA_gop_balanced_budget` (consumer −, civ +) → `USA_gop_business_restoration` (+2 civ, PP) → `USA_gop_commitment` ("The Grand Old Party", wing flag, excl others) → `USA_gop_america_first` ✋State=isolationist → `USA_gop_neutrality_acts_teeth` → `USA_gop_fortress_america` (+forts, hemisphere defense spirit) → `USA_gop_hemisphere_patrol` → `USA_gop_reluctant_crusade` (requires at_war; bypass) vs `USA_gop_armed_neutrality` (excl pair) → `USA_gop_war_on_our_terms` → `USA_gop_dewey_dawn` ('44 challenge event `.115` tie-in).

'45–'56: fork `USA_gop_mr_republican` (Taft; excl `USA_gop_eastern_establishment`) → Taft line: `USA_gop_fortress_doctrine`, `USA_gop_bring_the_boys_home` (demobilize: −mil, +civ, stability), `USA_gop_hemisphere_imperium_light` (Latin trade bloc), `USA_gop_mccarthy_unleashed` ✋AG=security (PP +, stability −, rad wing blocked) ;; Establishment line: `USA_gop_eastern_establishment` → `USA_gop_vandenberg_moment` (bipartisan containment; unlocks dem_marshall_plan co-req alternative `USA_gop_marshall_votes`), `USA_gop_ike_draft` ('52: leader Ike GOP), `USA_gop_dynamic_conservatism` (+stability +civ), `USA_gop_mccarthy_censured` (stability +5, requires Establishment).

- [ ] **Step 1: '36–'44 focuses + loc + validate + commit** — `git commit -m "gop wing: 1936-44 — rollback, America First, Fortress America"`
- [ ] **Step 2: '45–'56 focuses + loc + validate + commit** — `git commit -m "gop wing: 1945-56 — Taft vs the Establishment"`

---

### Task 8: Radical wing (≈30, two sub-tasks)

'36–'44: `USA_rad_voices` anchor child pair **stem fork**: `USA_rad_share_our_wealth` (Long-populist; excl `USA_rad_popular_front`) / `USA_rad_popular_front` (CPUSA-CIO). Common ladder: `USA_rad_sit_down_wave` (mil/civ penalty, org +), `USA_rad_general_strike` (event `.210` showdown), `USA_rad_commitment` ("The People's Front", wing flag) → government: `USA_rad_peoples_front_government` (leader swap event `.211`, ideology shift) → fork **`USA_rad_workers_democracy`** (democratic socialist: keep elections, stability ladder, `USA_rad_economic_bill_of_rights`, `USA_rad_one_big_union`) vs **`USA_rad_vanguard`** ✋AG=security (party state: `USA_rad_smash_the_reaction` purge event `.212`, −stability +PP, elections suspended → trunk elections bypass via flag) ;; war story: `USA_rad_premature_antifascists` (early intervention: war goal vs fascist majors unlocked '38!), `USA_rad_peoples_war` (+manpower, partisans).

'45–'56: democratic line → `USA_rad_third_camp` (independent socialist America: nonaligned spirit, trade) / vanguard line → `USA_rad_comintern_pivot` (faction with SOV possible) → shared: `USA_rad_atomic_secrets_shared` (event choice; world tension), `USA_rad_red_half_century` capstones per line.

- [ ] **Steps: '36–'44 → loc → validate → commit** `git commit -m "rad wing: 1936-44 — Share Our Wealth to the People's Front"`; **'45–'56 → loc → validate → commit** `git commit -m "rad wing: 1945-56 — Workers' Democracy vs the Vanguard"`

---

### Task 9: Authoritarian wing (≈30, two sub-tasks)

'36–'44: `USA_auth_whispers` anchor child → crisis stem (`USA_auth_veterans_grievance`, `USA_auth_business_backers`) → **fork**: `USA_auth_business_plot` (junta; excl `USA_auth_silver_legion`) / `USA_auth_silver_legion` (movement) → `USA_auth_commitment` ("The American Caesar" / takes Third-Term-Crisis or Suspended-Election trunk focus as alt-prereq, wing flag, leader event `.215` MacArthur or Pelley) → consolidation: `USA_auth_crush_labor` (−stability, +factory output), `USA_auth_new_order_at_home` ✋AG=loyalist (secret police spirit), `USA_auth_loyalty_oaths`, `USA_auth_press_brought_to_heel` → expansion: `USA_auth_hemisphere_destiny` (claims Latin neighbors), `USA_auth_good_neighbor_with_teeth` (puppet CSA/MEX path), `USA_auth_war_on_our_schedule` (war goals at choice).

'45–'56: `USA_auth_pax_americana` (postwar hegemony spirit) → `USA_auth_tribute_system` (trade exploitation), `USA_auth_legions_overseas` (forward bases), `USA_auth_atomic_diplomacy` ✋War=loyalist (threaten with the Bomb event `.216`), capstone `USA_auth_imperium` (rename country flavor, ideology cemented) + a fragile-throne counterweight (`USA_auth_succession_question` event `.217` — junta infighting if stability low).

- [ ] **Steps: two sub-task commits as above** — `"auth wing: 1936-44 — the Plot and the Legion"`, `"auth wing: 1945-56 — Pax Americana to Imperium"`

---

### Task 10: Military pillar (≈25)

Date-floor-gated ladder usable by all wings (no wing prereqs; ✋ none): industry (`USA_mil_arsenal_question` anchor → `USA_mil_war_resources_board`, `USA_mil_synthetic_rubber`, `USA_mil_liberty_fleet` convoys, `USA_mil_willow_run` +mil) · navy (`USA_mil_two_ocean_navy` → `USA_mil_carrier_doctrine`, `USA_mil_essex_program`, `USA_mil_fleet_train`) · air (`USA_mil_air_corps_expansion` → `USA_mil_very_long_range` B-29, `USA_mil_strategic_air_command` '46+, `USA_mil_jet_transition` '45+, `USA_mil_century_series` '54+) · atomic (`USA_mil_uranium_committee` '39+ → `USA_mil_manhattan_project` (research bonus + nuke spirit) → `USA_mil_trinity` (1 nuke + event `.220`) → `USA_mil_the_super` '50+ → `USA_mil_atoms_underwater` Nautilus '54) · Korea-era (`USA_mil_rotation_system`, `USA_mil_helicopter_age`).

- [ ] **Steps: focuses → loc → validate → commit** — `git commit -m "military pillar: mobilization to the Super"`

---

### Task 11: Cabinet slates '40–'52 (~32 ideas + appointment focuses)

**Files:** ideas, national_focus (appointment focuses under each era's trunk row), effects (`USA_clear_cabinet` grows), loc

- [ ] **Step 1: Slate tables.** Each era × wing-in-power: 4 seats × 2 candidates. Dem '40: State Hull/Welles, Treasury Morgenthau/Jones, War Stimson/Johnson, AG Jackson/Biddle. Dem '48: State Marshall/Byrnes, Treasury Snyder/Douglas, Defense Forrestal/Johnson, AG Clark/McGrath. GOP '48/'52: State Dulles/Taft-man, Treasury Humphrey/banker, Defense Wilson/MacArthur(!), AG Brownell/security-hawk. Ike '52 slate doubles for dem_ike path. Rad: Foreign Sec Browder/Thomas, etc. Auth: junta picks MacArthur-men vs Legion ideologues (8 ideas each pole). Every idea: portrait via vanilla GFX where the person exists (`GFX_idea_george_marshall` etc.), generic minister otherwise; modifiers small and seat-appropriate (State: opinion/trade; Treasury: consumer/civ; War: XP/doctrine cost; AG: stability/resistance).
- [ ] **Step 2: Appointment focuses** per slate (2-candidate mut-excl pairs, ✋ unlocked by that era's election event), each `USA_fill_cabinet_seat` + pole shift, as Task 3's pattern.
- [ ] **Step 3: `USA_clear_cabinet` updated with every new idea id.**
- [ ] **Step 4: Loc (names + descs for ~32 ideas and ~32 focuses), validate, commit** — `git commit -m "cabinet: era slates 1940-52 for all wings"`

---

### Task 12: Scripted localisation for balance poles + wing spirits polish

- [ ] **Step 1:** `common/scripted_localisation/usa_cabinet_scripted_loc.txt` — `USA_cabinet_balance_left_name`/`_right_name` keyed on wing flags (Progressives/Old Guard default; Loyalists/Fellow Travelers when `USA_wing_rad`; Junta/Movement when `USA_wing_auth`). Reference from the power-balance loc keys.
- [ ] **Step 2:** Validate, commit — `git commit -m "cabinet: per-wing balance pole names via scripted loc"`

---

### Task 13: Final sweep — README, descriptor, acceptance

- [ ] **Step 1:** Full validator run: `python3 tools/validate_mod.py usa_presidential_cabinet` → CLEAN. Then grep-audit: every `✋` cabinet gate in this plan exists in script (`grep -c has_idea` roughly ≥ 25), focus count `grep -c 'focus = {'` ≥ 165.
- [ ] **Step 2:** README rewrite (feature table per wing, the five elections, RT56 note), `descriptor.mod` → `version="0.3.0"`, supported_version unchanged.
- [ ] **Step 3:** `./install.sh usa_presidential_cabinet` and hand off to the user for the in-game acceptance pass (tree renders, '36 election fires, cabinet portraits show, no error.log entries from `usa_cabinet`).
- [ ] **Step 4:** Commit + PR — `git commit -m "docs: v0.3.0 Wings of the Eagle"`, branch `feat/wings-of-the-eagle`, PR to main.

---

## Self-review notes

- Spec coverage: trunk(T2–4), dem(T5–6), gop(T7), rad(T8), auth(T9), military(T10), cabinet slates+gating(T3,T11), scripted balance loc(T12), validator(T1), README/acceptance(T13). Focus budget: 6 skeleton + ~14 trunk + 9 cabinet '36 + 35 dem + 30 gop + 30 rad + 30 auth + 25 mil + ~32 era appointments ≈ 211 blocks (>170 because appointment focuses count separately) — within spirit of spec; trim during wing implementation only if the canvas gets cramped, never below 170.
- Type/name consistency: era flags `USA_era_*`, wing flags `USA_wing_*`, idea prefix `USA_cab_*`, events `usa_cabinet.100–299` used consistently above.
- Descriptions: every roster row carries a desc brief; loc steps say "final prose, period voice" — no deferred placeholders.
