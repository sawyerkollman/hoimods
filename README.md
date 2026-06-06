# Presidential Cabinet — A USA Overhaul (HOI4)

A standalone focus tree for the **United States** in Hearts of Iron IV. It
replaces the vanilla US tree with a new one built around a **Presidential
Cabinet / "inner circle"** system inspired by Germany's Götterdämmerung
mechanic, plus a layered historical-and-alternate-history spine that gives
the United States real depth **beyond 1942** (postwar planning, Bretton
Woods, the UN, the Marshall Plan, and the opening moves of the Cold War).

## Features

### The Brain Trust (the cabinet / inner circle)
Assemble FDR's inner circle through focuses. Each of four cabinet seats has
two **mutually exclusive** candidates pulling the administration toward the
**Progressive / New Deal** pole or the **Old Guard / Conservative** pole:

| Seat | Progressive pick | Conservative pick |
|------|------------------|-------------------|
| Secretary of State | Cordell Hull (internationalist) | An Isolationist |
| Secretary of the Treasury | Henry Morgenthau | A Man of Business |
| Secretary of War | Henry Stimson | Harry Woodring |
| Attorney General | Frank Murphy | A Security Hawk |

Every appointment grants that member as a **national-spirit idea** (so the
cabinet shows as a row of "inner circle" portraits with their own bonuses)
and shifts a **Cabinet power balance** (Progressives ⟷ Old Guard). The
make-up of your cabinet then unlocks divergent paths.

### Layered historical + alternate-history paths
- **Historical spine:** A Nation Rebuilds → Second New Deal → Total
  Mobilization (1941+) → Manhattan Project → Postwar Planning → Bretton
  Woods → United Nations → Marshall Plan → Iron Curtain → **Containment vs.
  Return to Normalcy**, capped by *The American Century*.
- **Progressive offshoots:** Economic Bill of Rights, and (deep progressive)
  *A Cooperative Commonwealth*.
- **Conservative / reactionary offshoots:** Restore the Old Republic, and
  (deep conservative) *The American Caesar*.
- **Demobilization vs. a Permanent Military Establishment** after the war.

## How the cabinet mechanic is implemented

- The cabinet is **focus-driven** (as requested), with mutually-exclusive
  candidate focuses per seat.
- Appointees and milestones are **national-spirit ideas** (`common/ideas`).
- Internal struggle is shown by a **power balance** (`common/power_balance`).
- **Crucially, every branching path is gated on hidden influence
  _variables_** (`USA_progressive_influence` / `USA_conservative_influence` /
  `USA_cabinet_seats_filled`), not on the power balance. This means the tree
  and cabinet remain fully functional even if a particular game version
  handles power-balance scripting differently — the power balance is purely a
  flavour indicator.

## Requirements / compatibility

- Designed against a **Götterdämmerung-era** install (the power balance and
  inner-circle framing assume that DLC's systems). The variable-gated core
  works without it; only the power-balance meter depends on newer scripting.
- Replaces the vanilla USA national focus tree (it out-weights it for tag
  USA), so it is **not compatible** with other mods that overhaul the US
  tree.
- `supported_version` is set to `1.16.*`. If you are on a different patch,
  edit `descriptor.mod` — the launcher only warns, it will still load.

## Installation

1. Copy this repository's contents into a folder under your HOI4 mod
   directory, e.g.:
   `Documents/Paradox Interactive/Hearts of Iron IV/mod/usa_cabinet/`
2. Create a launcher descriptor next to that folder named
   `usa_cabinet.mod` containing:

   ```
   version="0.1.0"
   tags={ "Alternative History" "Gameplay" "National Focuses" }
   name="Presidential Cabinet - A USA Overhaul"
   supported_version="1.16.*"
   path="mod/usa_cabinet"
   ```
3. Launch HOI4, enable the mod in the Playset, and start as the USA.

## File layout

```
descriptor.mod
common/national_focus/usa_cabinet.txt        # the focus tree
common/ideas/usa_cabinet_ideas.txt           # cabinet members + spirits
common/power_balance/usa_cabinet_power_balance.txt
common/scripted_effects/usa_cabinet_effects.txt
common/on_actions/usa_cabinet_on_actions.txt # variable init at game start
events/usa_cabinet_events.txt                # flavour events
localisation/english/usa_cabinet_l_english.yml
```

## Known limitations / next steps

- No custom art yet — focuses reuse vanilla goal icons and ideas use default
  portraits. Drop sprites into `gfx/interface/` and wire them up to brand it.
- Cabinet members are spirits, not recruitable advisor *characters*; a future
  pass could promote them to full character/advisor definitions with
  portraits.
- The alt-history paths set ideology popularity but do not yet force full
  government changes, civil wars, or unique war goals — natural areas to
  expand.

This is a v0.1 foundation: it loads as a coherent, internally-consistent
tree. Because it can't be play-tested in this environment, load it once in
your own game and check the error log (`logs/error.log`) for any
version-specific tweaks.
