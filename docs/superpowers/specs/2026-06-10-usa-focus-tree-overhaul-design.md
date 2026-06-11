# USA Focus Tree Overhaul — "Wings of the Eagle" (1936–1956)

**Mod:** `mods/usa_presidential_cabinet` (Presidential Cabinet — A USA Overhaul)
**Date:** 2026-06-10
**Status:** Approved design, pending implementation plan

## Goal

Replace the current 53-focus tree with a fully fleshed-out ~170-focus tree
covering 1936–1956, with a written description for **every** focus. Deep
historical spine plus genuine alt-history branches (conservative, radical-left,
authoritarian), with the cabinet/inner-circle mechanic as the centerpiece of
every path. Stays a Road to 56 submod.

## Decisions made (with the user)

| Question | Decision |
|---|---|
| Scope | Full overhaul: deep historical spine AND alt-history wings, ~170 focuses |
| Alt-history range | Plausible politics + authoritarian extreme + radical-left extreme; no sandbox absurdities |
| Cabinet mechanic | Centerpiece of ALL paths; every administration assembles a cabinet; composition gates focuses |
| Era structure | Election-era chapters: 1936/40/44/48/52 elections as chapter breaks with cabinet turnover |
| Dependency | Remains a Road to 56 submod (guarded references; degrade gracefully) |
| Military content | One shared military-industrial pillar (~25 focuses); no per-ideology military branches |
| Macro-layout | **A — Wings of the Eagle** (chosen visually): central trunk, ideology wings fanning out, military pillar on the edge, era bands top→bottom |

## Macro-layout

Vertical axis is time (1936 top → 1956 bottom), five era bands. Horizontal
order, left → right:

```
RADICAL wing | DEMOCRATIC wing | TRUNK (cabinet+elections) | REPUBLICAN wing | AUTHORITARIAN wing | MILITARY pillar
```

Each wing hangs off `relative_position_id` anchor focuses (one per wing) so a
whole wing can be repositioned by editing a single focus.

## Content inventory (focus budget ≈ 170)

### Trunk — shared spine (~20)

- 1936 opener: **The Inheritance of '32** (root).
- Election anchors: **The Election of 1936 / 1940 / 1944 / 1948 / 1952** —
  date-gated (available within ~6 months of the historical date), each fires
  an election event chain (see Mechanics) and triggers cabinet turnover.
- War-entry pivot (**A Date Which Will Live in Infamy** / alt triggers) and
  peace-conference pivot (**The Shape of the Peace**).
- Authoritarian on-ramps live in the trunk as dark alternatives at two
  elections: **The Third Term Crisis** (1940) and **The Suspended Election**
  (1944).

### Democratic wing (~35) — the historical play

Clusters: Second New Deal → Court fight (**Nine Old Men**) → rearmament
politics → **Cash and Carry** → **Lend-Lease** → **Arsenal of Democracy** →
war mobilization (WPB, OSRD) → wartime diplomacy (Atlantic Charter, Tehran,
Yalta) → **The President Is Dead** (Truman succession) → V-E/V-J →
**Bretton Woods**, **The United Nations** → **Truman Doctrine** →
**The Marshall Plan** → **NATO** → Fair Deal → Korea → the '52 handoff
(**I Like Ike** vs **The Egghead** — Stevenson) → New Look, Atoms for Peace,
**The Interstate System**.

### Republican wing (~30) — constitutional conservatism

Clusters: Landon '36 → New Deal rollback (business restoration, balanced
budget) → **America First** isolationism → **Fortress America** (hemisphere
defense) → reluctant war entry after Pearl Harbor OR armed neutrality held →
the fork: **Mr. Republican** (Taft isolationism into the '50s) vs
**The Eastern Establishment** (Dewey/Ike internationalism rejoining
containment) → McCarthy-era content on both sub-paths.

### Radical wing (~30) — the American left

Stem: **Share Our Wealth** populism or CPUSA organizing → labor militancy
(sit-down strikes, a national general strike) → **The People's Front**
government → fork: **Democratic socialism** (workers' democracy, civil
liberties retained) vs **The Vanguard** (party state, security purges) →
early anti-fascist intervention as its war story → postwar: Comintern
alignment vs an independent socialist America.

### Authoritarian wing (~30) — the American Caesar

Stem: shared crisis cluster → fork: **The Business Plot** (corporatist
junta, MacArthur as Caesar) vs **The Silver Legion** (genuine fascist
movement, Pelley/Coughlinite) → crush labor → New Order at home →
opportunist hemisphere expansion → war on its own terms → **Pax Americana**
→ **Imperium**.

### Military pillar (~25) — shared by all paths

Industrial mobilization ladder → **The Two-Ocean Navy** → carrier doctrine →
strategic air → **The Manhattan Project** → the Bomb → SAC → **The Super**
(H-bomb) → jet age → Korea-era modernization. Era-gated by date floors so
every path uses it across the whole 20 years.

## Mechanics

### Cabinet (generalized from the existing 4 seats)

- Seats: **State, Treasury, War, Attorney General**. Two mutually exclusive
  candidates per seat, per administration (the existing pattern, made era- and
  ideology-aware).
- Each appointment = a national-spirit "inner circle" idea (portrait + bonus)
  and a shift on the **Cabinet power balance**.
- Power-balance pole names vary by wing: Progressives ⟷ Old Guard
  (Dem/GOP), Party Loyalists ⟷ Fellow Travelers (radical), Junta ⟷ Movement
  (authoritarian). Implementation: **one** power balance whose side names use
  scripted localisation keyed on the wing flag. Only if scripted loc proves
  unworkable for balance side names does the fallback (three separate
  balances, swapped via scripted effect at wing commitment) apply.
- Example slates: FDR '36 = Hull/isolationist, Morgenthau/businessman,
  Stimson/Woodring, Murphy/security-hawk (current mod's slate, kept).
  Truman '48 = Marshall vs Byrnes at State, etc. Strongman = MacArthur
  loyalists vs Legion ideologues.

### Cabinet gating

Roughly **a third of wing focuses carry a cabinet condition** in addition to
wing prerequisites. Canonical examples: Lend-Lease requires internationalist
State; Fortress America requires the isolationist; the vanguard purge path
requires the security AG.

### Elections as chapter breaks

- Trunk election focus completes → event chain fires. Options shown depend on:
  (a) wing investment, (b) power-balance position, (c) story flags (at war?).
- Outcome: leader change (or continuity) + **cabinet reset** (all seat spirits
  cleared via scripted effect) + next era's appointment focuses unlock.
- Not holding an election is the authoritarian on-ramp (Third Term Crisis '40,
  Suspended Election '44).

### Era unlocks

Later era bands require: prior era's election anchor completed **+ date
floor**. War-dependent focuses additionally check world-state flags with
alt-history fallbacks (e.g., if the war ended differently, postwar offers
"a Cold Peace" variants instead of dead-ending).

### Wing commitment

Opening wing focuses are free to sample. Each wing has a **commitment focus
~3 deep** that hard-excludes the other wings' commitment focuses and recolors
the administration (ruling-party/ideology shifts happen here and at election
events, not on entry focuses).

## Technical architecture

| File | Content |
|---|---|
| `common/national_focus/usa_cabinet.txt` | Full tree (~170 focuses), commented sections: TRUNK / DEM / GOP / RADICAL / AUTH / MILITARY; per-wing `relative_position_id` anchors |
| `common/ideas/usa_cabinet_ideas.txt` | ~40 cabinet spirits across all eras/slates; vanilla/RT56 portrait GFX, generic minister portraits otherwise |
| `common/power_balance/usa_cabinet_power_balance.txt` | The cabinet balance(s) per the implementation choice above |
| `events/usa_cabinet_events.txt` | ~35 events: election chains '36–'52, coup/succession, era transitions |
| `common/scripted_effects/usa_cabinet_effects.txt` | cabinet-clear, election-outcome resolver, era-flag setters |
| `common/on_actions/usa_cabinet_on_actions.txt` | startup wiring, date pulses |
| `localisation/english/usa_cabinet_l_english.yml` | Name + 1–3 sentence period-voice description for **every** focus; full event loc (~700+ lines) |

### RT56 compatibility

Only USA-tag content is overridden; everything namespaced `usa_cabinet_*`; no
defines or shared-file edits. References to RT56 advisor/tech ids are
`if`-guarded so the mod degrades gracefully when RT56 changes.

### Validation — `tools/validate_mod.py` (new, checked into repo)

Plain-python linter run before every commit, asserting:

1. Balanced braces / parseable Paradox script.
2. Focus `id`s unique; every `prerequisite`, `relative_position_id`,
   `mutually_exclusive` references an existing focus.
3. No two focuses resolve to the same (x, y) cell.
4. Every focus and idea has loc keys **including `_desc`**.
5. Every event id fired by a focus/effect exists in the events file.
6. `.yml` files are UTF-8 with BOM (regression guard for the past blank-
   descriptions bug).

Final acceptance: user launches HOI4, eyeballs the tree, plays through one
election chain.

## Out of scope

- Custom GFX/icons (map to vanilla/RT56 GFX keys only).
- AI strategy beyond a basic historical-path weighting.
- Non-English localisation.
- The `more_dockyards_per_line` mod (untouched).

## Acceptance criteria

- ~170 focuses, all with `_desc` localisation, validator clean.
- All five elections playable with cabinet turnover on each.
- Each wing completable 1936→1956 without dead ends, war or no war.
- Mod loads under RT56 current version with zero error.log entries from our
  files.
