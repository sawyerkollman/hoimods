# Presidential Cabinet — A USA Expansion (HOI4)

An expansion **built around the full vanilla United States focus tree** (all
~135 vanilla focuses — Congress, the war plans, the civil-war alt-history
paths, and every doctrine branch — are kept intact) that grafts on **62 new
focuses**: a Götterdämmerung-style **Presidential Cabinet / inner circle**
system, a **post-1942 Cold War endgame**, and — the heart of the expansion —
**new deep branches off the non-historical routes**.

## Features (197 focuses total: 135 vanilla + 62 new)

### The Brain Trust (the cabinet / inner circle)
Assemble FDR's inner circle through focuses, in a new cluster alongside the
vanilla tree. Four contested seats each offer two **mutually exclusive**
candidates pulling toward the **Progressive / New Deal** pole or the **Old
Guard / Conservative** pole, plus two more historic appointments:

| Seat | Progressive pick | Conservative pick |
|------|------------------|-------------------|
| Secretary of State | Cordell Hull (internationalist) | An Isolationist |
| Secretary of the Treasury | Henry Morgenthau | A Man of Business |
| Secretary of War | Henry Stimson | Harry Woodring |
| Attorney General | Frank Murphy | A Security Hawk |
| Secretary of Labor | Frances Perkins | — |
| Secretary of the Navy | — | Frank Knox |

Every appointment grants that member as a **national-spirit idea** and
shifts a **Cabinet power balance** (Progressives ⟷ Old Guard). Cabinet
make-up gates the Progressive Ascendancy / Conservative Resurgence forks,
the Economic Bill of Rights, and *The President's Men* capstone.

### The People's Republic — communist path expansion
Picks up where vanilla's communist civil-war victory ends (*Reintegration /
Unholy Alliance / Secure China*): proclaim the **People's Republic of
America** (cosmetic tag), collectivize the Great Plains, empower workers'
councils, then choose — **Look to Moscow** (Comintern alignment) or **An
American Road to Socialism** (found your own faction, *The Continental
International*, and spread revolution across the hemisphere), capped by
*The Workers' Century*.

### The Silver Republic — fascist path expansion
Picks up from *Honor the Confederacy / Recruit the Free Corps*: proclaim the
**Silver Republic of America** (cosmetic tag), impose the Leader Principle
and the Corporate State, then choose — **An Understanding with Berlin** (the
Atlantic Axis) or **America Stands Alone** (found *The Silver Pact* and
ultimately claim a **war goal against Germany** as *A Rival New Order*),
capped by *The Silver Century*.

### The Business of America — conservative-democratic mini-branch
Extends the gold-standard route: Wall Street Resurgent, the Republican
Restoration, and An Engine of Prosperity.

### The Postwar Order — the democratic endgame (beyond 1942)
Anchored to vanilla's *The Giant Wakes*: Postwar Planning → Bretton Woods /
United Nations → Shape the Peace → Marshall Plan / Iron Curtain →
**Containment vs. Return to Normalcy** and **Demobilization vs. a Permanent
Establishment**, capped by *The American Century* (requires your Inner
Circle).

### About the base tree
The vanilla tree included here is taken from the community game-file mirror
[hoi4-history](https://github.com/cbrzeczysz/hoi4-history) at game version
**1.14.1** (the US tree has been essentially stable since Man the Guns). If
a future patch changes the vanilla US tree, you can refresh the base: copy
`common/national_focus/usa.txt` from your game install (e.g.
`steamapps/common/Hearts of Iron IV/common/national_focus/usa.txt`) over
this mod's copy and re-apply the graft section (everything below the
`PRESIDENTIAL CABINET EXPANSION` banner comment).

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

- **Road to 56 submod.** This mod declares **Road to 56** as a dependency
  (`dependencies` in `descriptor.mod`) so the launcher loads R56 first and
  this mod on top. You must **subscribe to Road to 56 yourself** — none of
  R56's files are copied or redistributed here. With R56 active, the focus
  tree's tech bonuses feed R56's extended late-war / Cold War trees, and the
  R&D branch (extra research slot + research speed) lets you actually reach
  them.
  - The focus tech bonuses use **vanilla research _categories_**
    (industry, electronics, nuclear, doctrines), which automatically cover
    whatever extended techs R56 adds in those categories — no fragile
    references to R56-specific technology IDs.
  - It will still load **without** R56; you simply won't have the extended
    trees, only the deeper research bonuses.
- Designed against a **Götterdämmerung-era** install (the power balance and
  inner-circle framing assume that DLC's systems). The variable-gated core
  works without it; only the power-balance meter depends on newer scripting.
- Replaces the vanilla USA national focus tree (it out-weights it for tag
  USA), so it is **not compatible** with other mods that overhaul the US
  tree.
- `supported_version` is set to `1.16.*`. If you are on a different patch,
  edit `descriptor.mod` — the launcher only warns, it will still load.

### Load order

In the launcher Playset, order them top-to-bottom:

```
Road to 56
Presidential Cabinet - A USA Overhaul   (this mod, loaded last)
```

## Installation

**Easiest (Windows):** from the repo root, run the installer — it copies this
mod into your HOI4 mod folder and creates the launcher pointer for you:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Mod usa_presidential_cabinet
```

**Manual:** copy both of these from the repo's `mods\` folder into your HOI4
mod directory (`Documents\Paradox Interactive\Hearts of Iron IV\mod\`):

- the `usa_presidential_cabinet\` folder
- the `usa_presidential_cabinet.mod` pointer file (already set with
  `path="mod/usa_presidential_cabinet"`)

Then subscribe to **Road to 56** on the Steam Workshop, launch HOI4, enable
both mods in a Playset (Road to 56 above this mod), and start as the USA.

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
